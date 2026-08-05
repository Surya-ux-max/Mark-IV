"""Conversation behavior — explain gestures while speaking."""

from __future__ import annotations

from typing import Any

from app.animation.hands.hand_controller import HandController
from app.robot.behaviors.base_behavior import BaseBehavior


class ConversationBehavior(BaseBehavior):
    def __init__(self, hand_controller: HandController) -> None:
        self._hands = hand_controller

    @property
    def name(self) -> str:
        return "conversation"

    async def execute(self, context: Any) -> None:
        await self._hands.explain()
