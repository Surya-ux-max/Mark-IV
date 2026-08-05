"""Greeting state — robot just woke up and delivers greeting."""

from __future__ import annotations

import random
from typing import Any, Optional

from app.config.constants import RobotState
from app.config.robot import RobotConfig
from app.events.event_types import EventType
from app.events.publishers import RobotPublisher
from app.robot.state_machine.base_state import BaseState


class GreetingState(BaseState):
    """Robot delivers wake-up greeting then transitions to Idle."""

    _config = RobotConfig()

    @property
    def state_id(self) -> RobotState:
        return RobotState.GREETING

    async def on_enter(self, context: Any) -> None:
        await super().on_enter(context)
        greeting = random.choice(self._config.wake_phrases)
        await RobotPublisher.started_speaking(greeting)

    async def handle_event(
        self, event_type: str, payload: Any, context: Any
    ) -> Optional[str]:
        if event_type == EventType.ROBOT_STOPPED_SPEAKING:
            return RobotState.IDLE
        if event_type == EventType.COMMAND_RECEIVED:
            if payload.get("command") == "SLEEP":
                return RobotState.SLEEPING
        return None
