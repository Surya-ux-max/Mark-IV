"""Async event bus — the central nervous system of SurveX.

All inter-module communication goes through this bus.
Modules publish events; other modules subscribe to them.
This eliminates direct dependencies between subsystems.

Usage:
    bus = EventBus()
    bus.subscribe(EventType.USER_MESSAGE_RECEIVED, my_handler)
    await bus.publish(EventType.USER_MESSAGE_RECEIVED, payload)
"""

from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import Any, Callable, Coroutine, Dict, List

from app.core.logging import get_logger
from app.events.event_types import EventType

logger = get_logger(__name__)

HandlerType = Callable[[str, Any], Coroutine[Any, Any, None]]


class EventBus:
    """Async publish-subscribe event bus.

    - Handlers are async coroutines.
    - All handlers for an event run concurrently via asyncio.gather.
    - Errors in one handler do not affect others.
    """

    def __init__(self) -> None:
        self._handlers: Dict[str, List[HandlerType]] = defaultdict(list)
        self._lock = asyncio.Lock()

    def subscribe(self, event_type: EventType | str, handler: HandlerType) -> None:
        """Register an async handler for an event type."""
        key = event_type.value if isinstance(event_type, EventType) else event_type
        self._handlers[key].append(handler)
        logger.debug("event_subscribed", evt=key, handler=handler.__name__)

    def unsubscribe(self, event_type: EventType | str, handler: HandlerType) -> None:
        """Remove a handler from an event type."""
        key = event_type.value if isinstance(event_type, EventType) else event_type
        self._handlers[key] = [h for h in self._handlers[key] if h is not handler]

    async def publish(self, event_type: EventType | str, payload: Any = None) -> None:
        """Publish an event to all registered handlers concurrently."""
        key = event_type.value if isinstance(event_type, EventType) else event_type
        handlers = self._handlers.get(key, [])

        if not handlers:
            logger.debug("event_no_handlers", evt=key)
            return

        logger.debug("event_published", evt=key, handler_count=len(handlers))

        results = await asyncio.gather(
            *[self._safe_call(handler, key, payload) for handler in handlers],
            return_exceptions=True,
        )

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(
                    "event_handler_error",
                    evt=key,
                    handler=handlers[i].__name__,
                    error=str(result),
                )

    async def _safe_call(
        self, handler: HandlerType, event_type: str, payload: Any
    ) -> None:
        """Invoke a single handler, catching all exceptions."""
        try:
            await handler(event_type, payload)
        except Exception as exc:
            raise exc

    def clear(self) -> None:
        """Remove all subscriptions."""
        self._handlers.clear()

    @property
    def subscription_count(self) -> int:
        return sum(len(handlers) for handlers in self._handlers.values())


# Module-level singleton shared across the application
event_bus = EventBus()
