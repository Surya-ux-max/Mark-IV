"""Error state — robot encountered an error and needs recovery."""

from __future__ import annotations

from typing import Any, Optional

from app.config.constants import RobotState
from app.events.event_types import EventType
from app.robot.state_machine.base_state import BaseState


class ErrorState(BaseState):
    """Robot encountered an error. Can recover via RESET or WAKE_UP command."""

    @property
    def state_id(self) -> RobotState:
        return RobotState.ERROR

    async def handle_event(
        self, event_type: str, payload: Any, context: Any
    ) -> Optional[str]:
        if event_type == EventType.COMMAND_RECEIVED:
            cmd = payload.get("command", "")
            if cmd in ("RESET", "WAKE_UP"):
                return RobotState.IDLE
            if cmd == "SLEEP":
                return RobotState.SLEEPING
        return None
