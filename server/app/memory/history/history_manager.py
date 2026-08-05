"""History manager — manages per-session conversation histories."""

from __future__ import annotations

from typing import Dict, List, Optional

from app.core.logging import get_logger
from app.memory.history.history_store import HistoryStore
from app.models.messages import ConversationTurn

logger = get_logger(__name__)


class HistoryManager:
    """Manages multiple per-session conversation histories."""

    def __init__(self, max_turns: int = 10) -> None:
        self._max_turns = max_turns
        self._sessions: Dict[str, HistoryStore] = {}

    def _get_or_create(self, session_id: str) -> HistoryStore:
        if session_id not in self._sessions:
            self._sessions[session_id] = HistoryStore(max_turns=self._max_turns)
            logger.debug("history_session_created", session_id=session_id)
        return self._sessions[session_id]

    def add_turn(self, session_id: str, turn: ConversationTurn) -> None:
        """Record a conversation turn for a session."""
        store = self._get_or_create(session_id)
        store.add(turn)

    def get_groq_messages(self, session_id: str) -> List[dict]:
        """Get Groq-formatted message history for a session."""
        if session_id not in self._sessions:
            return []
        return self._sessions[session_id].to_groq_messages()

    def clear_session(self, session_id: str) -> None:
        """Clear history for a specific session."""
        if session_id in self._sessions:
            self._sessions[session_id].clear()
            logger.debug("history_session_cleared", session_id=session_id)

    def remove_session(self, session_id: str) -> None:
        """Remove a session entirely."""
        self._sessions.pop(session_id, None)
        logger.debug("history_session_removed", session_id=session_id)

    @property
    def active_sessions(self) -> int:
        return len(self._sessions)
