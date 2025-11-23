import sys
import asyncio
from spoon_ai.chat import ChatBot
from adaptive_agent import AdaptiveAgent

async def main():
    agent = AdaptiveAgent(ChatBot(model_name="gemini-2.5-flash", llm_provider="gemini", temperature=0.1))

    if sys.stdin.isatty():
        while True:
            try:
                prompt = await asyncio.to_thread(input, "> ")
            except EOFError:
                break
            prompt = prompt.strip()
            if not prompt:
                continue
            if prompt.lower() in {"exit", "quit"}:
                break
            result = await agent.run(prompt)
            print(result, flush=True)
    else:
        for line in sys.stdin:
            prompt = line.strip()
            if not prompt:
                continue
            result = await agent.run(prompt)
            print(result, flush=True)

if __name__ == "__main__":
    asyncio.run(main())