"""Response parser — post-processes raw LLM output."""

from __future__ import annotations

import re


def clean_response(raw: str) -> str:
    """Strip markdown artifacts and normalize whitespace."""
    # Remove leading/trailing whitespace
    text = raw.strip()

    # Remove markdown headers (## Title)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove markdown bold/italic markers for TTS clarity
    text = re.sub(r"\*{1,2}(.*?)\*{1,2}", r"\1", text)

    return text.strip()


def extract_intent_hint(text: str) -> str:
    """Very lightweight intent hint from LLM output (not a full NLU)."""
    lower = text.lower()
    if any(w in lower for w in ["hello", "hi", "hey", "greet"]):
        return "GREETING"
    if any(w in lower for w in ["bye", "goodbye", "see you", "farewell"]):
        return "FAREWELL"
    if "?" in text:
        return "QUESTION"
    return "STATEMENT"
