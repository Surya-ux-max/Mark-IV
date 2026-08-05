"""LLM-specific configuration helpers."""

from dataclasses import dataclass
from app.config.settings import Settings


@dataclass(frozen=True)
class LLMConfig:
    """Immutable LLM configuration snapshot."""

    api_key: str
    model: str
    temperature: float
    max_tokens: int

    @classmethod
    def from_settings(cls, settings: Settings) -> "LLMConfig":
        return cls(
            api_key=settings.groq_api_key,
            model=settings.groq_model,
            temperature=settings.groq_temperature,
            max_tokens=settings.groq_max_tokens,
        )
