import uvicorn
import asyncio
from typing import Dict, List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from spoon_ai.chat import ChatBot
from adaptive_agent import AdaptiveAgent
import time

app = FastAPI()

# 1. CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. MODELS
class ChatRequest(BaseModel):
    message: str
    session_id: str = "demo-session-default"

class ChatResponse(BaseModel):
    response: str
    tools: List[str]
    is_reflex: bool
    time_taken: float

# 3. SESSION MANAGEMENT
agent_sessions: Dict[str, AdaptiveAgent] = {}

def get_or_create_agent(session_id: str):
    if session_id not in agent_sessions:
        print(f"Initializing new Adaptive Agent for session: {session_id}")
        chatbot = ChatBot(model_name="gemini-2.5-flash", llm_provider="gemini", temperature=0.1)
        agent_sessions[session_id] = AdaptiveAgent(chatbot)
    return agent_sessions[session_id]

# 4. ENDPOINTS
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        agent = get_or_create_agent(request.session_id)
        
        # Added timeout to prevent hanging
        result_text = await asyncio.wait_for(agent.run(request.message), timeout=60)
        tools_before = len(agent.available_tools.tool_map) if hasattr(agent.available_tools, "tool_map") else 0
        start_time = time.time()
        result_text = await asyncio.wait_for(agent.run(request.message), timeout=60) # idk if this is right 
        duration = time.time() - start_time

        tools_after = len(agent.available_tools.tool_map) if hasattr(agent.available_tools, "tool_map") else 0
        is_reflex = tools_after == tools_before
        
        current_tools = []
        if hasattr(agent.available_tools, "tool_map"):
            current_tools = list(agent.available_tools.tool_map.keys())
        
        return ChatResponse(
            response=str(result_text),
            tools=current_tools,
            is_reflex = is_reflex,
            time_taken = duration
        )

    except Exception as e:
        msg = str(e)
        if "api key" in msg.lower():
            raise HTTPException(status_code=400, detail="LLM provider API key missing or invalid")
        raise HTTPException(status_code=500, detail=msg)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    # Pre-warm the default agent so the first request isn't slow
    print("Pre-loading default agent...")
    agent = get_or_create_agent("demo-session-default")
    try:
        if hasattr(agent, "initialize"):
            agent.initialize()
    except Exception as e:
        print(f"Startup warning: {e}")

# start server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)