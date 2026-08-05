"""Pydantic models for robot state, emotion, and pose."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.config.constants import Emotion, RobotState


class EmotionSnapshot(BaseModel):
    """Current emotion with intensity."""

    emotion: Emotion = Emotion.NEUTRAL
    intensity: float = Field(ge=0.0, le=1.0, default=0.5)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class RobotStateSnapshot(BaseModel):
    """Complete snapshot of the robot's current state."""

    state: RobotState = RobotState.SLEEPING
    emotion: EmotionSnapshot = Field(default_factory=EmotionSnapshot)
    is_awake: bool = False
    is_speaking: bool = False
    is_listening: bool = False
    session_id: Optional[str] = None
    uptime_seconds: float = 0.0
    updated_at: datetime = Field(default_factory=datetime.utcnow)
