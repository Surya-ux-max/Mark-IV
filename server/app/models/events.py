"""Pydantic models for all event payloads."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class BaseEvent(BaseModel):
    """Base class for all event payloads."""

    timestamp: datetime = Field(default_factory=datetime.utcnow)
    session_id: Optional[str] = None


class UserMessageEvent(BaseEvent):
    text: str
    language: str = "en"


class RobotResponseEvent(BaseEvent):
    text: str
    emotion: str = "NEUTRAL"
    sources: list[str] = Field(default_factory=list)


class StateChangedEvent(BaseEvent):
    previous_state: str
    new_state: str
    emotion: str = "NEUTRAL"


class EmotionChangedEvent(BaseEvent):
    emotion: str
    intensity: float = Field(ge=0.0, le=1.0, default=0.5)
    trigger: Optional[str] = None


class AnimationCueEvent(BaseEvent):
    animation: str
    params: Dict[str, Any] = Field(default_factory=dict)
    duration_ms: Optional[int] = None


class FaceDetectedEvent(BaseEvent):
    face_id: str
    position: Dict[str, float] = Field(default_factory=dict)
    confidence: float = 1.0


class ErrorEvent(BaseEvent):
    message: str
    code: str = "ERROR"
