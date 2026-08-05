"""Abstract base interfaces for all injectable services.

Every major service implements one of these interfaces, enabling
dependency injection, mocking in tests, and future hardware swaps.
"""

from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, List, Optional


class IService(ABC):
    """Base interface for all services."""

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the service (connect, load, etc.)."""

    @abstractmethod
    async def shutdown(self) -> None:
        """Gracefully shut down the service."""


class ILLMService(IService):
    """Interface for LLM inference services."""

    @abstractmethod
    async def generate(
        self,
        system_prompt: str,
        messages: List[dict],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate a text response from the LLM."""

    @abstractmethod
    async def generate_stream(
        self,
        system_prompt: str,
        messages: List[dict],
    ) -> AsyncIterator[str]:
        """Stream tokens from the LLM."""


class IKnowledgeRetriever(ABC):
    """Interface for knowledge retrieval services."""

    @abstractmethod
    async def retrieve(self, query: str, top_k: int = 2) -> List[Any]:
        """Retrieve top-k relevant knowledge documents for a query."""


class ISTTService(IService):
    """Interface for Speech-to-Text services."""

    @abstractmethod
    async def transcribe(self, audio_data: bytes) -> str:
        """Transcribe audio bytes to text."""


class ITTSService(IService):
    """Interface for Text-to-Speech services."""

    @abstractmethod
    async def synthesize(self, text: str) -> bytes:
        """Synthesize text to audio bytes."""


class IEventBus(ABC):
    """Interface for the event bus."""

    @abstractmethod
    async def publish(self, event_type: str, payload: Any) -> None:
        """Publish an event to all subscribers."""

    @abstractmethod
    def subscribe(self, event_type: str, handler: Any) -> None:
        """Register a handler for an event type."""


class IState(ABC):
    """Interface for robot states in the FSM."""

    @abstractmethod
    async def on_enter(self, context: Any) -> None:
        """Called when entering this state."""

    @abstractmethod
    async def on_exit(self, context: Any) -> None:
        """Called when leaving this state."""

    @abstractmethod
    async def handle_event(self, event_type: str, payload: Any, context: Any) -> Optional[str]:
        """Handle an event. Return the name of the next state, or None to stay."""
