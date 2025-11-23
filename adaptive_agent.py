from spoon_ai.agents import ToolCallAgent
from spoon_ai.tools.tool_manager import ToolManager
from spoon_ai.chat import ChatBot
from generation_tool import GenerationTool
from dynamic_tool_loader import load_generated_tools

class AdaptiveAgent(ToolCallAgent):
    name: str = "adaptive_agent"
    description: str = "User-facing assistant"
    system_prompt: str = "You are a helpful assistant. You will recieve the ability to generate tools to help the user." \
    "Your aim is to minimize the amount of work the user must do. Only ask for implementation details that are strictly necessary, like missing keys." \
    "Any other implementation details should be handled by yourself. You should never tell the user you have the ability to generate tools," \
    "but rather simply process the query to the best of your ability. If you generate a tool, you will recieve another prompt from the system." \
    "instructing you on how to use it. If the task generation fails, generate a final response with a detailed error log." \
    "Be aware that your tools can only take in string inputs currently!"
    max_steps: int = 10

    def __init__(self, llm: ChatBot):
        tool_manager = ToolManager([])
        tool_manager.add_tool(GenerationTool(llm))
        super().__init__(llm=llm, available_tools=tool_manager)

    def initialize(self):
        try:
            print("Attempting to load new tools.")
            load_generated_tools(self.available_tools)
        except Exception as e:
            print(e)
            pass

    async def step(self):
        self.initialize()
        await super().step()