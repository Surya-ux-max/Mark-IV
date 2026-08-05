"""Base behavior — abstract class all behaviors inherit from."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseBehavior(ABC):
    """Abstract base for all robot behaviors."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique behavior identifier."""

    @abstractmethod
    async def execute(self, context: Any) -> None:
        """Run the behavior."""

    async def on_interrupt(self) -> None:
        """Called when this behavior is interrupted by another."""
