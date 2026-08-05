"""Pydantic model for a knowledge document."""

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Document(BaseModel):
    """A parsed knowledge base document."""

    doc_id: str
    title: str
    category: str = "General"
    short_name: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    content: str
    file_path: str
    score: float = 0.0  # set during retrieval

    def to_context_block(self) -> str:
        """Format document as a context block for LLM injection."""
        return (
            f"[Source: {self.title}]\n"
            f"{self.content.strip()}\n"
        )
