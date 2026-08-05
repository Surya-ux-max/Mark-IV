"""Intent detector — classifies user message intent without an external NLU."""

from __future__ import annotations

from app.config.constants import IntentType

_GREETING_WORDS = {"hello", "hi", "hey", "howdy", "good morning", "good afternoon", "good evening"}
_FAREWELL_WORDS = {"bye", "goodbye", "see you", "farewell", "good night", "take care", "later"}
_KNOWLEDGE_WORDS = {
    "peo", "po", "pso", "program", "outcome", "objective", "curriculum",
    "mission", "vision", "career", "scope", "syllabus", "subject",
    "course", "department", "cse", "computer", "placement", "job",
}
_COMMAND_WORDS = {"wake", "sleep", "stop", "pause", "reset", "quiet"}


def detect_intent(text: str) -> IntentType:
    """Classify the user's intent from their message text."""
    lower = text.lower().strip()
    tokens = set(lower.split())

    if any(w in lower for w in _FAREWELL_WORDS):
        return IntentType.FAREWELL

    if any(w in lower for w in _GREETING_WORDS):
        return IntentType.GREETING

    if any(w in lower for w in _COMMAND_WORDS):
        return IntentType.COMMAND

    if tokens & _KNOWLEDGE_WORDS or "?" in lower:
        if tokens & _KNOWLEDGE_WORDS:
            return IntentType.KNOWLEDGE_QUERY
        return IntentType.QUESTION

    if len(lower) < 20 and "?" not in lower:
        return IntentType.CHITCHAT

    return IntentType.UNKNOWN
