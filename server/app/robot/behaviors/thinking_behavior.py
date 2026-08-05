"""Thinking behavior — thinking pose while processing."""

from __future__ import annotations

from typing import Any

from app.animation.hands.hand_controller import HandController
from app.robot.behaviors.base_behavior import BaseBehavior
from app.events.event_bus import event_bus
from app.events.event_types import EventType


class ThinkingBehavior(BaseBehavior):
    def __init__(self, hand_controller: HandController) -> None:
        self._hands = hand_controller

    @property
    def name(self) -> str:
        return "thinking"

    async def execute(self, context: Any) -> None:
        await self._hands.thinking_pose()
        await event_bus.publish(
            EventType.HEAD_TILT,
            {"direction": "right", "intensity": 0.5},
        )
        await event_bus.publish(
            EventType.LOOK_UP,
            {"intensity": 0.6},
        )
