import uvicorn
import asyncio
from typing import Dict, List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from spoon_ai.chat import ChatBot
from adaptive_agent import AdaptiveAgent
import time

# --- SESSION MANAGEMENT ---
agent_sessions: Dict[str, AdaptiveAgent] = {}

def get_or_create_agent(session_id: str):
    if session_id not in agent_sessions:
        print(f"Initializing new Adaptive Agent for session: {session_id}")
        chatbot = ChatBot(model_name="gemini-2.5-flash", llm_provider="gemini", temperature=0.1)
        agent_sessions[session_id] = AdaptiveAgent(chatbot)
    return agent_sessions[session_id]

# --- LIFESPAN HANDLER ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Wrapped in try/except so a broken agent doesn't crash the entire server on startup
    try:
        print("Pre-loading default agent...")
        agent = get_or_create_agent("demo-session-default")
        if hasattr(agent, "initialize"):
            agent.initialize()
    except Exception as e:
        print(f"⚠️ Startup Warning: Failed to pre-load agent. Server will start anyway.\nError: {e}")
    yield

app = FastAPI(lifespan=lifespan)

# --- CORS ---
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

# --- MODELS ---
class ChatRequest(BaseModel):
    message: str
    session_id: str = "demo-session-default"

class ChatResponse(BaseModel):
    response: str
    tools: List[str]
    is_reflex: bool
    time_taken: float

# --- HELPER FUNCTIONS ---
def get_tool_count(agent) -> int:
    """Safely get tool count without crashing if tools are missing or malformed"""
    try:
        # Check if available_tools exists
        if not hasattr(agent, "available_tools") or not agent.available_tools:
            return 0
            
        # Case A: available_tools is a ToolManager (has tool_map)
        if hasattr(agent.available_tools, "tool_map"):
            return len(agent.available_tools.tool_map)
            
        # Case B: available_tools is a list
        if isinstance(agent.available_tools, list):
            return len(agent.available_tools)
            
    except Exception:
        # If anything weird happens (like AttributeErrors), just return 0
        return 0
    return 0

def get_tool_names(agent) -> List[str]:
    """Safely get tool names without crashing"""
    try:
        if not hasattr(agent, "available_tools") or not agent.available_tools:
            return []

        # Case A: ToolManager
        if hasattr(agent.available_tools, "tool_map"):
            return list(agent.available_tools.tool_map.keys())
            
        # Case B: List of tools
        if isinstance(agent.available_tools, list):
            # Only try to access .name if it exists
            return [t.name for t in agent.available_tools if hasattr(t, 'name')]
            
    except Exception:
        return []
    return []

# --- ENDPOINTS ---
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # This might raise an error if AdaptiveAgent init fails, caught below
        agent = get_or_create_agent(request.session_id)
        
        # 1. Safe Snapshot before (will return 0 if failed)
        tools_before = get_tool_count(agent)
        
        start_time = time.time()
        
        # 2. Run Agent
        result_text = await asyncio.wait_for(agent.run(request.message), timeout=60)
        
        duration = time.time() - start_time

        # 3. Safe Snapshot after
        tools_after = get_tool_count(agent)
        
        # 4. Determine Reflex (did we gain a tool?)
        is_reflex = tools_after > tools_before
        
        current_tools = get_tool_names(agent)
        
        return ChatResponse(
            response=str(result_text),
            tools=current_tools,
            is_reflex=is_reflex,
            time_taken=duration
        )

    except Exception as e:
        msg = str(e)
        print(f"Error processing request: {msg}")
        if "api key" in msg.lower():
            raise HTTPException(status_code=400, detail="LLM provider API key missing or invalid")
        raise HTTPException(status_code=500, detail=f"Agent Error: {msg}")

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)