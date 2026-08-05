"""Context builder — formats retrieved documents into LLM-injectable context."""

from __future__ import annotations

from typing import List

from app.models.knowledge import Document


def build_context_block(documents: List[Document], max_chars: int = 2000) -> str:
    """Format top-k documents into a context string for the system prompt.

    Args:
        documents: Ranked documents (already top-k).
        max_chars: Maximum total character length for the context block.

    Returns:
        Formatted context string ready to inject into the system prompt.
    """
    if not documents:
        return ""

    parts = ["## Relevant Knowledge\n"]
    total = len(parts[0])

    for doc in documents:
        block = doc.to_context_block()
        if total + len(block) > max_chars:
            # Truncate last block to fit
            remaining = max_chars - total
            if remaining > 100:
                parts.append(block[:remaining] + "...\n")
            break
        parts.append(block)
        total += len(block)

    return "\n".join(parts)


def get_source_titles(documents: List[Document]) -> List[str]:
    """Extract document titles for source attribution."""
    return [doc.title for doc in documents]
