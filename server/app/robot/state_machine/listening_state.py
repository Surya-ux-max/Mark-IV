"""Listening state — robot is actively listening to the user."""

from __future__ import annotations

from typing import Any, Optional

from app.config.constants import RobotState
from app.events.event_types import EventType
from app.robot.state_machine.base_state import BaseState


class ListeningState(BaseState):
    """Robot is actively listening."""

    @property
    def state_id(self) -> RobotState:
        return RobotState.LISTENING

    async def handle_event(
        self, event_type: str, payload: Any, context: Any
    ) -> Optional[str]:
        if event_type == EventType.USER_STOPPED_SPEAKING:
            return RobotState.THINKING
        if event_type == EventType.USER_MESSAGE_RECEIVED:
            return RobotState.THINKING
        if event_type == EventType.COMMAND_RECEIVED:
            if payload.get("command") == "SLEEP":
                return RobotState.SLEEPING
        return None
