"""Pydantic models for chat messages and conversation turns."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    """A single message in a conversation."""

    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    session_id: Optional[str] = None


class ConversationTurn(BaseModel):
    """A complete user→robot exchange."""

    user_text: str
    robot_text: str
    emotion: str = "NEUTRAL"
    intent: str = "UNKNOWN"
    knowledge_sources: list[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class WSIncomingMessage(BaseModel):
    """WebSocket message from client → server."""

    type: str
    text: Optional[str] = None
    command: Optional[str] = None
    session_id: Optional[str] = None
    data: Optional[dict] = None


class WSOutgoingMessage(BaseModel):
    """WebSocket message from server → client."""

    type: str
    data: dict = Field(default_factory=dict)
