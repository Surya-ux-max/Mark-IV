"""Master application settings loaded from .env via pydantic-settings."""

from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── LLM ──────────────────────────────────────────────────────────────────
    groq_api_key: str = Field(..., description="Groq API key")
    groq_model: str = Field("llama-3.3-70b-versatile", description="Groq model name")
    groq_temperature: float = Field(0.7, ge=0.0, le=2.0)
    groq_max_tokens: int = Field(512, ge=64, le=4096)

    # ── Robot ─────────────────────────────────────────────────────────────────
    robot_name: str = Field("Surya", description="Robot's display name")
    robot_personality: str = Field(
        "helpful, warm, curious, and professional",
        description="Personality descriptor injected into system prompt",
    )

    # ── Server ────────────────────────────────────────────────────────────────
    server_host: str = Field("0.0.0.0")
    server_port: int = Field(8000)
    log_level: str = Field("INFO")

    # ── Knowledge Base ────────────────────────────────────────────────────────
    knowledge_path: str = Field("./knowledge")
    top_k_docs: int = Field(2, ge=1, le=5)

    # ── History ───────────────────────────────────────────────────────────────
    max_history_turns: int = Field(10, ge=1, le=50)

    # ── CORS ──────────────────────────────────────────────────────────────────
    cors_origins: str = Field(
        "http://localhost:5173,http://localhost:3000",
        description="Comma-separated list of allowed CORS origins",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str) -> str:
        return v

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached singleton Settings instance."""
    return Settings()
