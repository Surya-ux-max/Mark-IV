"""Observing state — robot notices a face and may initiate greeting."""

from __future__ import annotations

from typing import Any, Optional

from app.config.constants import RobotState
from app.events.event_types import EventType
from app.robot.state_machine.base_state import BaseState


class ObservingState(BaseState):
    """Robot is observing (face detected, waiting for interaction)."""

    @property
    def state_id(self) -> RobotState:
        return RobotState.OBSERVING

    async def handle_event(
        self, event_type: str, payload: Any, context: Any
    ) -> Optional[str]:
        if event_type == EventType.USER_MESSAGE_RECEIVED:
            return RobotState.THINKING
        if event_type == EventType.USER_STARTED_SPEAKING:
            return RobotState.LISTENING
        if event_type == EventType.FACE_LOST:
            return RobotState.IDLE
        if event_type == EventType.COMMAND_RECEIVED:
            if payload.get("command") == "SLEEP":
                return RobotState.SLEEPING
        return None
