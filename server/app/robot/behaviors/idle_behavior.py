"""Idle behavior — natural idle animations when robot has nothing to do."""

from __future__ import annotations

import asyncio
import random
from typing import Any

from app.animation.hands.hand_controller import HandController
from app.animation.legs.leg_controller import LegController
from app.robot.behaviors.base_behavior import BaseBehavior


_IDLE_GESTURES = ["idle", "fold", "hands_behind"]


class IdleBehavior(BaseBehavior):
    def __init__(
        self,
        hand_controller: HandController,
        leg_controller: LegController,
    ) -> None:
        self._hands = hand_controller
        self._legs = leg_controller

    @property
    def name(self) -> str:
        return "idle"

    async def execute(self, context: Any) -> None:
        gesture = random.choice(_IDLE_GESTURES)
        await self._hands.play(gesture)
        await self._legs.idle_stance()
