"""DI-injectable LLM service wrapping GroqClient."""

from __future__ import annotations

from typing import AsyncIterator, List, Optional

from app.core.interfaces import ILLMService, IService
from app.core.logging import get_logger
from app.services.llm.groq_client import GroqClient

logger = get_logger(__name__)


class LLMService(ILLMService):
    """Injectable LLM service. Depends on GroqClient."""

    def __init__(self, client: GroqClient) -> None:
        self._client = client

    async def initialize(self) -> None:
        logger.info("llm_service_ready", model=self._client._model)

    async def shutdown(self) -> None:
        logger.info("llm_service_shutdown")

    async def generate(
        self,
        system_prompt: str,
        messages: List[dict],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        return await self._client.complete(
            system_prompt=system_prompt,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    async def generate_stream(
        self,
        system_prompt: str,
        messages: List[dict],
    ) -> AsyncIterator[str]:
        return self._client.stream(system_prompt=system_prompt, messages=messages)
