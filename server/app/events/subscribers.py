"""Subscriber base class and decorator for event handlers."""

from __future__ import annotations

import asyncio
from functools import wraps
from typing import Any, Callable, List

from app.events.event_bus import event_bus
from app.events.event_types import EventType


class EventSubscriber:
    """Base class for objects that subscribe to events.

    Subclasses define handler methods decorated with @on(EventType.XYZ).
    Call subscribe_all() to register all handlers with the event bus.

    Example:
        class MyModule(EventSubscriber):
            @on(EventType.USER_MESSAGE_RECEIVED)
            async def handle_message(self, event_type: str, payload: dict) -> None:
                ...
    """

    def subscribe_all(self) -> None:
        """Register all @on-decorated methods with the event bus."""
        for attr_name in dir(self):
            method = getattr(self, attr_name, None)
            if callable(method) and hasattr(method, "_event_type"):
                event_bus.subscribe(method._event_type, method)


def on(event_type: EventType) -> Callable:
    """Decorator to mark a method as an event handler."""

    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            return await fn(*args, **kwargs)

        wrapper._event_type = event_type
        return wrapper

    return decorator
