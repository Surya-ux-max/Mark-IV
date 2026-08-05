"""Text utility functions."""

from __future__ import annotations

import re


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to max_length, appending suffix if truncated."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def normalize_whitespace(text: str) -> str:
    """Replace multiple spaces/newlines with single space."""
    return re.sub(r"\s+", " ", text).strip()


def word_count(text: str) -> int:
    """Count words in text."""
    return len(text.split())
