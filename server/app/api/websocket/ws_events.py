"""WebSocket event schemas — the contract between server and client."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


# ── Outgoing (server → client) ─────────────────────────────────────────────

class StateChangedMessage(BaseModel):
    type: str = "STATE_CHANGED"
    state: str
    emotion: str = "NEUTRAL"
    is_awake: bool = False


class RobotResponseMessage(BaseModel):
    type: str = "ROBOT_RESPONSE"
    text: str
    session_id: Optional[str] = None
    sources: List[str] = []


class EmotionChangedMessage(BaseModel):
    type: str = "EMOTION_CHANGED"
    emotion: str
    intensity: float = 0.5


class AnimationCueMessage(BaseModel):
    type: str = "ANIMATION_CUE"
    animation: str
    params: Dict[str, Any] = {}
    duration_ms: Optional[int] = None


class WelcomeMessage(BaseModel):
    type: str = "WELCOME"
    session_id: str
    robot_name: str
    state: str
    message: str = "Connected to SurveX Robot Server"


class ErrorMessage(BaseModel):
    type: str = "ERROR"
    message: str
    code: str = "ERROR"


class PongMessage(BaseModel):
    type: str = "PONG"


# ── Incoming (client → server) ─────────────────────────────────────────────

class IncomingWSMessage(BaseModel):
    type: str
    text: Optional[str] = None
    command: Optional[str] = None
    session_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
