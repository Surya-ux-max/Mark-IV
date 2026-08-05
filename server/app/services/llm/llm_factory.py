"""LLM service factory — creates a configured GroqClient."""

from __future__ import annotations

from app.config.settings import Settings
from app.services.llm.groq_client import GroqClient


def create_groq_client(settings: Settings) -> GroqClient:
    """Instantiate a GroqClient from application settings."""
    return GroqClient(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=settings.groq_temperature,
        max_tokens=settings.groq_max_tokens,
    )
