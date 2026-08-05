"""REST chat endpoint — fallback for non-WebSocket clients."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.dependencies.get_services import get_conversation_manager, get_robot_controller

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    message: str
    session_id: str = "rest-default"


class ChatResponse(BaseModel):
    response: str
    intent: str
    sources: list[str]
    emotion: str


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    conversation_manager=Depends(get_conversation_manager),
    robot_controller=Depends(get_robot_controller),
) -> ChatResponse:
    """Send a text message and get a response (REST fallback)."""
    if not robot_controller.is_awake:
        raise HTTPException(status_code=400, detail="Robot is sleeping. Wake it up first.")

    result = await conversation_manager.process(request.message, request.session_id)
    return ChatResponse(
        response=result.response_text,
        intent=result.intent,
        sources=result.knowledge_sources,
        emotion=result.emotion_hint,
    )
