"""Speaking state — robot is delivering its response."""

from __future__ import annotations

from typing import Any, Optional

from app.config.constants import RobotState
from app.events.event_types import EventType
from app.robot.state_machine.base_state import BaseState


class SpeakingState(BaseState):
    """Robot is speaking its response."""

    @property
    def state_id(self) -> RobotState:
        return RobotState.SPEAKING

    async def handle_event(
        self, event_type: str, payload: Any, context: Any
    ) -> Optional[str]:
        if event_type == EventType.ROBOT_STOPPED_SPEAKING:
            return RobotState.IDLE
        if event_type == EventType.COMMAND_RECEIVED:
            cmd = payload.get("command", "")
            if cmd == "STOP_SPEAKING":
                return RobotState.IDLE
            if cmd == "SLEEP":
                return RobotState.SLEEPING
        return None
