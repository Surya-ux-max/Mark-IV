"""Greeting behavior — wave + smile + say hello."""

from __future__ import annotations

import random
from typing import Any

from app.animation.hands.hand_controller import HandController
from app.robot.behaviors.base_behavior import BaseBehavior
from app.events.event_bus import event_bus
from app.events.event_types import EventType


_GREETINGS = [
    "Hello! I'm Surya, your CSE department assistant. How can I help you today?",
    "Hi there! Welcome to the CSE department. I'm Surya, ready to assist!",
    "Namaste! I'm Surya. Ask me anything about our CSE program!",
]


class GreetingBehavior(BaseBehavior):
    def __init__(self, hand_controller: HandController) -> None:
        self._hands = hand_controller

    @property
    def name(self) -> str:
        return "greeting"

    async def execute(self, context: Any) -> None:
        session_id = context.get("session_id", "default") if context else "default"
        # Wave + greeting text simultaneously
        await self._hands.wave(intensity=0.9)
        text = random.choice(_GREETINGS)
        await event_bus.publish(
            EventType.ROBOT_STARTED_SPEAKING,
            {"text": text, "session_id": session_id},
        )
