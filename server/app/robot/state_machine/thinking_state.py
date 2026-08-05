"""Thinking state — robot is processing the user's message with the LLM."""

from __future__ import annotations

from typing import Any, Optional

from app.config.constants import RobotState
from app.events.event_types import EventType
from app.robot.state_machine.base_state import BaseState


class ThinkingState(BaseState):
    """Robot is thinking (LLM processing)."""

    @property
    def state_id(self) -> RobotState:
        return RobotState.THINKING

    async def handle_event(
        self, event_type: str, payload: Any, context: Any
    ) -> Optional[str]:
        if event_type == EventType.LLM_RESPONSE_READY:
            return RobotState.SPEAKING
        if event_type == EventType.SYSTEM_ERROR:
            return RobotState.ERROR
        return None
