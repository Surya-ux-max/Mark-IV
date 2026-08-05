"""Idle state — robot is awake and waiting for input."""

from __future__ import annotations

from typing import Any, Optional

from app.config.constants import RobotState
from app.events.event_types import EventType
from app.robot.state_machine.base_state import BaseState


class IdleState(BaseState):
    """Robot is awake, idle, and ready to listen."""

    @property
    def state_id(self) -> RobotState:
        return RobotState.IDLE

    async def handle_event(
        self, event_type: str, payload: Any, context: Any
    ) -> Optional[str]:
        if event_type == EventType.USER_STARTED_SPEAKING:
            return RobotState.LISTENING
        if event_type == EventType.USER_MESSAGE_RECEIVED:
            return RobotState.THINKING
        if event_type == EventType.FACE_DETECTED:
            return RobotState.OBSERVING
        if event_type == EventType.COMMAND_RECEIVED:
            if payload.get("command") == "SLEEP":
                return RobotState.SLEEPING
        return None
