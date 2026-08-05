"""Emotion memory — stores recent emotional history for context.

Allows the engine to make smarter decisions based on emotional trajectory
(e.g., avoid rapid back-and-forth between emotions).
"""

from __future__ import annotations

from collections import deque
from datetime import datetime
from typing import Deque, List, Optional, Tuple

from app.emotion.states.emotion_state import EmotionState, EmotionType


class EmotionMemory:
    """Ring buffer of recent emotion states."""

    def __init__(self, capacity: int = 20) -> None:
        self._history: Deque[Tuple[datetime, EmotionState]] = deque(maxlen=capacity)

    def record(self, state: EmotionState) -> None:
        self._history.append((datetime.utcnow(), state))

    def recent_emotions(self, n: int = 5) -> List[EmotionType]:
        """Return the last n emotion types in chronological order."""
        entries = list(self._history)[-n:]
        return [state.emotion for _, state in entries]

    def last_state(self) -> Optional[EmotionState]:
        if not self._history:
            return None
        return self._history[-1][1]

    def has_been_in(self, emotion: EmotionType, within_last: int = 5) -> bool:
        """Return True if emotion appeared in the last N recorded states."""
        return emotion in self.recent_emotions(within_last)

    def clear(self) -> None:
        self._history.clear()

    @property
    def size(self) -> int:
        return len(self._history)
