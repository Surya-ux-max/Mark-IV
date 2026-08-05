"""Sleeping state — robot is dormant, ignores most events."""

from __future__ import annotations

from typing import Any, Optional

from app.config.constants import RobotState
from app.events.event_types import EventType
from app.robot.state_machine.base_state import BaseState


class SleepingState(BaseState):
    """Robot is sleeping. Only WAKE_UP command wakes it."""

    @property
    def state_id(self) -> RobotState:
        return RobotState.SLEEPING

    async def handle_event(
        self, event_type: str, payload: Any, context: Any
    ) -> Optional[str]:
        if event_type == EventType.COMMAND_RECEIVED:
            cmd = payload.get("command", "")
            if cmd == "WAKE_UP":
                return RobotState.GREETING
        return None
