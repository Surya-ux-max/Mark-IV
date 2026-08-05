"""Behavior manager — selects and executes the right behavior for each context.

Maps robot states and intent types to concrete behavior classes.
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional

from app.animation.hands.hand_controller import HandController
from app.animation.legs.leg_controller import LegController
from app.core.logging import get_logger
from app.robot.behaviors.base_behavior import BaseBehavior
from app.robot.behaviors.conversation_behavior import ConversationBehavior
from app.robot.behaviors.farewell_behavior import FarewellBehavior
from app.robot.behaviors.greeting_behavior import GreetingBehavior
from app.robot.behaviors.idle_behavior import IdleBehavior
from app.robot.behaviors.listening_behavior import ListeningBehavior
from app.robot.behaviors.thinking_behavior import ThinkingBehavior

logger = get_logger(__name__)


class BehaviorManager:
    """Selects and executes contextually appropriate robot behaviors."""

    def __init__(
        self,
        hand_controller: HandController,
        leg_controller: LegController,
    ) -> None:
        self._hands = hand_controller
        self._legs = leg_controller
        self._current_behavior: Optional[BaseBehavior] = None

        self._behaviors: Dict[str, BaseBehavior] = {
            "greeting":     GreetingBehavior(hand_controller),
            "thinking":     ThinkingBehavior(hand_controller),
            "listening":    ListeningBehavior(hand_controller),
            "conversation": ConversationBehavior(hand_controller),
            "idle":         IdleBehavior(hand_controller, leg_controller),
            "farewell":     FarewellBehavior(hand_controller),
        }

    async def trigger(self, behavior_name: str, context: Any = None) -> None:
        """Execute a named behavior."""
        behavior = self._behaviors.get(behavior_name)
        if not behavior:
            logger.warning("behavior_not_found", behavior=behavior_name)
            return

        if self._current_behavior:
            await self._current_behavior.on_interrupt()

        self._current_behavior = behavior
        logger.info("behavior_started", behavior=behavior_name)

        try:
            await behavior.execute(context)
        except Exception as exc:
            logger.error("behavior_error", behavior=behavior_name, error=str(exc))
        finally:
            if self._current_behavior is behavior:
                self._current_behavior = None

    async def on_robot_state_changed(self, event_type: str, payload: Any) -> None:
        """Auto-trigger behavior based on new robot state."""
        new_state = payload.get("new_state", "")
        context = payload

        state_to_behavior = {
            "GREETING":  "greeting",
            "THINKING":  "thinking",
            "LISTENING": "listening",
            "SPEAKING":  "conversation",
            "IDLE":      "idle",
        }

        behavior_name = state_to_behavior.get(new_state)
        if behavior_name:
            asyncio.create_task(self.trigger(behavior_name, context))

    @property
    def active_behavior(self) -> Optional[str]:
        return self._current_behavior.name if self._current_behavior else None
