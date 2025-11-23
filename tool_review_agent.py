from spoon_ai.agents.base import BaseAgent
from spoon_ai.chat import ChatBot
from spoon_ai.schema import AgentState

class RetoolAgent(BaseAgent):
    def __init__(self, llm:ChatBot):
        super().__init__(name="retool", llm=llm, system_prompt="You are a retooling agent. " \
        "You are given a previous iteration of a tool and what needs to be rebuilt in it." \
        "The tool should be a python function that takes in the specified inputs, and outputs the specified outputs as a tuple." \
        "Never output code that wold not run in production - no example cases or anything. " \
        "In addition to outputting the function, create another asynchronous function called `run` that calls the function with the same inputs. This is for compatability." \
        "Your run code should only take string inputs. If necessary, parse the input before running it through any logic." \
        "You are permitted to import non standard pip modules. To do so, list pip modules in a commment at the end of your code output in a space separated list beginning with \"install modules:\"")
        self.max_steps=5

    async def step(self, run_id=None) -> str:
        reply = await self.llm.ask(system_msg = self.system_prompt, messages = self.memory.messages)
        reply = reply.strip("```").removeprefix("python")

        await self.add_message("assistant", reply)

        try: 
            compile(reply, '<string>', 'exec')
            self.state = AgentState.FINISHED
            return reply
        except SyntaxError as e:
            errorMsg = f"Syntax Error: {e.msg}\n" \
            f"Line: {e.lineno}: {e.text}\n" \
            f" {' ' * (e.offset - 1)}^"
            await self.add_message("tool", errorMsg)
            return reply + '\n' + errorMsg
