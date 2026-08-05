"""Thin typed wrapper around the Groq Python SDK."""

from __future__ import annotations

from typing import AsyncIterator, List, Optional

from groq import AsyncGroq

from app.core.exceptions import LLMException
from app.core.logging import get_logger

logger = get_logger(__name__)


class GroqClient:
    """Async Groq client wrapper with retry and error handling."""

    def __init__(self, api_key: str, model: str, temperature: float, max_tokens: int) -> None:
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._client = AsyncGroq(api_key=api_key)

    async def complete(
        self,
        system_prompt: str,
        messages: List[dict],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Send a chat completion request and return the full response text."""
        full_messages = [{"role": "system", "content": system_prompt}] + messages

        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=full_messages,
                temperature=temperature or self._temperature,
                max_tokens=max_tokens or self._max_tokens,
            )
            text = response.choices[0].message.content or ""
            logger.debug(
                "groq_completion",
                model=self._model,
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
            )
            return text.strip()

        except Exception as exc:
            logger.error("groq_completion_failed", error=str(exc))
            raise LLMException(f"Groq completion failed: {exc}") from exc

    async def stream(
        self,
        system_prompt: str,
        messages: List[dict],
    ) -> AsyncIterator[str]:
        """Stream tokens from Groq."""
        full_messages = [{"role": "system", "content": system_prompt}] + messages

        try:
            async with self._client.chat.completions.stream(
                model=self._model,
                messages=full_messages,
                temperature=self._temperature,
                max_tokens=self._max_tokens,
            ) as stream_ctx:
                async for chunk in stream_ctx:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        yield delta
        except Exception as exc:
            logger.error("groq_stream_failed", error=str(exc))
            raise LLMException(f"Groq streaming failed: {exc}") from exc
