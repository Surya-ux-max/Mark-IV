"""Farewell behavior — wave goodbye."""

from __future__ import annotations

from typing import Any

from app.animation.hands.hand_controller import HandController
from app.robot.behaviors.base_behavior import BaseBehavior
from app.events.event_bus import event_bus
from app.events.event_types import EventType


class FarewellBehavior(BaseBehavior):
    def __init__(self, hand_controller: HandController) -> None:
        self._hands = hand_controller

    @property
    def name(self) -> str:
        return "farewell"

    async def execute(self, context: Any) -> None:
        session_id = context.get("session_id", "default") if context else "default"
        await self._hands.play("bye", intensity=0.8)
        await event_bus.publish(
            EventType.ROBOT_STARTED_SPEAKING,
            {"text": "Goodbye! Have a great day! Feel free to come back anytime.", "session_id": session_id},
        )
