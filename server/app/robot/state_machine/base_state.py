"""Abstract base state for the robot FSM."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

from app.config.constants import RobotState
from app.core.logging import get_logger

logger = get_logger(__name__)


class BaseState(ABC):
    """Abstract base for all robot FSM states."""

    @property
    @abstractmethod
    def state_id(self) -> RobotState:
        """The RobotState enum value for this state."""

    async def on_enter(self, context: Any) -> None:
        """Called when entering this state. Override for entry actions."""
        logger.debug("state_entered", state=self.state_id)

    async def on_exit(self, context: Any) -> None:
        """Called when leaving this state. Override for cleanup."""
        logger.debug("state_exited", state=self.state_id)

    @abstractmethod
    async def handle_event(
        self, event_type: str, payload: Any, context: Any
    ) -> Optional[str]:
        """Handle an event. Return next state name, or None to stay."""
