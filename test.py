from generation_tool import GenerationTool
from spoon_ai.chat import ChatBot
import asyncio
import sys

# Defines Bus Problem
PROBLEM_DESC = """
Shuffles every letter in a string.
"""

async def main():
    agent = GenerationTool(ChatBot(model_name="gemini-2.5-pro", llm_provider="gemini", temperature=0.1))
    response = await agent.execute(f"name: \"souffle\", description: \"{PROBLEM_DESC}\", input: \"input: str\", output: \"output: str\"", "souffleTool")
    return response

async def balls():
    result = await souffleTool().execute("hello")
    return result

if __name__ == "__main__":
    result = asyncio.run(main())
    print(result)
    sys.path.insert(0, "generated-tools")
    from souffleTool import souffleTool
    result = asyncio.run(balls())
    print(result)