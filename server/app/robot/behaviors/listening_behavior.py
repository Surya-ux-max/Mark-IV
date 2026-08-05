"""Listening behavior — attentive pose while user speaks."""

from __future__ import annotations

from typing import Any

from app.animation.hands.hand_controller import HandController
from app.robot.behaviors.base_behavior import BaseBehavior
from app.events.event_bus import event_bus
from app.events.event_types import EventType


class ListeningBehavior(BaseBehavior):
    def __init__(self, hand_controller: HandController) -> None:
        self._hands = hand_controller

    @property
    def name(self) -> str:
        return "listening"

    async def execute(self, context: Any) -> None:
        await self._hands.fold_hands()
        await event_bus.publish(EventType.HEAD_NOD, {"intensity": 0.4})
