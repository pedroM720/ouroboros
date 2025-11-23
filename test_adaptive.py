import sys
import asyncio
from spoon_ai.chat import ChatBot
from adaptive_agent import AdaptiveAgent
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
#test adaptive
app = FastAPI()

origins = [
    "http://localhost:3000",  # allow local react app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def main():
    agent = AdaptiveAgent(ChatBot(model_name="gemini-3-pro", llm_provider="gemini", temperature=0.1))

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