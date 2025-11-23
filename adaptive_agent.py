import os
from spoon_ai.agents import ToolCallAgent
from spoon_ai.tools.tool_manager import ToolManager
from spoon_ai.chat import ChatBot
from dynamic_tool_loader import load_tool
from generation_tool import GenerationTool, ReTool
# adpative agent 
class AdaptiveAgent(ToolCallAgent):
    name: str = "adaptive_agent"
    description: str = "User-facing assistant"
    system_prompt: str = "You are a helpful assistant. You will recieve the ability to generate tools to help the user." \
    "Your aim is to minimize the amount of work the user must do. Only ask for implementation details that are strictly necessary, like missing keys." \
    "Any other implementation details should be handled by yourself. You should never tell the user you have the ability to generate tools," \
    "but rather simply process the query to the best of your ability. If you generate a tool, you will recieve another prompt from the system." \
    "instructing you on how to use it. If the task generation fails, generate a final response with a detailed error log." \
    "Here are some tips for generating tools:" \
    "Be aware that your tools can only take text input. Specify that it must be parsed, if it takes in abstract data types" \
    "Generalize your code as much as possible! For example, instead of counting the letter 'r' in a string, take in a letter as an input." \
    "Do not be afraid to create new tools, even for similar purposes. You want to help the user as much as possible, and generating tools that assist with that can help a lot." \
    "However, on the flip side, do not create a tool for everything. It should be aimed to solve problems that pure LLMs are bad at - like counting letters - or API interactions that you do not have access to." \
    "Do research into the best API to use before attempting to create a tool for it. Never say that you cannot do something unless you attempt tooling at least twice." \
    "If you are aware of a free API, that does not require keys, do your best to specify it to the tool creator. If it does require keys, still specify the API to use but prompt the user again for a key."
    max_steps: int = 10

    def __init__(self, llm: ChatBot):
        tool_manager = ToolManager([])
        tool_manager.add_tool(GenerationTool(llm, tool_manager))
        tool_manager.add_tool(ReTool(llm, tool_manager))
        super().__init__(llm=llm, available_tools=tool_manager)
        self._default_timeout = 300
        self.initialize()

    def initialize(self):
        try:
            for file in os.listdir("generated-tools"):
                if file.endswith(".py"):
                    load_tool(self.available_tools, os.path.join("generated-tools", file), file)
        except Exception as e:
            print(e)
            pass
