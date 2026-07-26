import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from langchain_core.messages import HumanMessage, AIMessage

# Import LangGraph workflow and Services
from graph.builder import build_survex_graph
from memory.service import MemoryService
from database.db import get_all_tasks, save_task

app = FastAPI(title="SurveX AI OS Multi-Agent Backend")

# Enable CORS for frontend client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    session_id: str
    input_type: str  # 'voice' or 'text'
    content: str

class ChatResponse(BaseModel):
    output_type: str  # 'both', 'text', 'voice'
    text: str
    voice: str
    metadata: Dict[str, Any]

class TaskUpdate(BaseModel):
    task_desc: str
    is_completed: bool

# Load graph instance on startup
survex_graph = build_survex_graph()

@app.get("/")
def read_root():
    return {"status": "ONLINE", "core": "SURVEX_LANGGRAPH_SUPERVISOR"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    query = request.content.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query content cannot be empty")

    session_id = request.session_id
    input_type = request.input_type
    start_time = time.time()

    try:
        # 1. Load only the last 6 messages for context (fast, bounded read)
        history = MemoryService.read_session_history(session_id)
        recent_history = history[-6:] if len(history) > 6 else history
        was_compressed = len(history) > 6

        # 2. Rebuild LangGraph message list
        graph_messages = []
        for msg in recent_history:
            if msg["sender"] == "operator":
                graph_messages.append(HumanMessage(content=msg["message"]))
            else:
                graph_messages.append(AIMessage(content=msg["message"]))
        graph_messages.append(HumanMessage(content=query))

        # 3. Build Graph inputs
        inputs = {
            "messages": graph_messages,
            "trace": [],
            "sender": "operator",
            "final_response": ""
        }
        config = {"configurable": {"thread_id": session_id}}

        # 4. Execute LangGraph (synchronous call — safe inside FastAPI async handler)
        output_state = survex_graph.invoke(inputs, config=config)

        final_reply = output_state.get("final_response", "Understood, Surya.")
        execution_trace = output_state.get("trace", [])
        latency_val = time.time() - start_time

        # 5. Persist messages to DB
        try:
            MemoryService.save_session_message(session_id, "operator", query, input_type=input_type, output_type="both")
            MemoryService.save_session_message(session_id, "survex", final_reply, input_type=input_type, output_type="both")
        except Exception as db_err:
            print(f"DB save warning: {db_err}")

        return {
            "output_type": "both",
            "text": final_reply,
            "voice": final_reply,
            "metadata": {
                "latency": f"{latency_val:.3f}s",
                "trace": execution_trace,
                "session_id": session_id,
                "input_type": input_type,
                "was_compressed": was_compressed
            }
        }

    except Exception as e:
        print(f"Chat route processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history")
async def get_history(session_id: str = "survex_default_session"):
    try:
        return MemoryService.read_session_history(session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tasks")
async def get_tasks():
    try:
        return get_all_tasks()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tasks")
async def add_task(task: TaskUpdate):
    try:
        save_task(task.task_desc, task.is_completed)
        return {"status": "SUCCESS"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
