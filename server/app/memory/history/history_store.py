"""Conversation history store — in-memory ring buffer of recent turns."""

from __future__ import annotations

from collections import deque
from typing import Deque, List

from app.models.messages import ConversationTurn


class HistoryStore:
    """Fixed-size ring buffer of conversation turns per session."""

    def __init__(self, max_turns: int = 10) -> None:
        self._max_turns = max_turns
        self._turns: Deque[ConversationTurn] = deque(maxlen=max_turns)

    def add(self, turn: ConversationTurn) -> None:
        """Append a conversation turn."""
        self._turns.append(turn)

    def get_all(self) -> List[ConversationTurn]:
        """Return all stored turns in chronological order."""
        return list(self._turns)

    def to_groq_messages(self) -> List[dict]:
        """Convert history to Groq-compatible message list format."""
        messages: List[dict] = []
        for turn in self._turns:
            messages.append({"role": "user", "content": turn.user_text})
            messages.append({"role": "assistant", "content": turn.robot_text})
        return messages

    def clear(self) -> None:
        """Clear all history."""
        self._turns.clear()

    @property
    def turn_count(self) -> int:
        return len(self._turns)

    @property
    def is_empty(self) -> bool:
        return len(self._turns) == 0
