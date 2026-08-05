"""Service registry — lightweight DI container.

Services are registered at startup and resolved by name or type.
This avoids circular imports by providing a central lookup point.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Type, TypeVar

T = TypeVar("T")


class ServiceRegistry:
    """Singleton service registry for dependency injection."""

    _instance: Optional["ServiceRegistry"] = None
    _services: Dict[str, Any] = {}

    def __new__(cls) -> "ServiceRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._services = {}
        return cls._instance

    def register(self, name: str, service: Any) -> None:
        """Register a service under a given name."""
        self._services[name] = service

    def get(self, name: str) -> Any:
        """Retrieve a service by name. Raises KeyError if not found."""
        if name not in self._services:
            raise KeyError(
                f"Service '{name}' not registered. "
                f"Available: {list(self._services.keys())}"
            )
        return self._services[name]

    def get_typed(self, name: str, expected_type: Type[T]) -> T:
        """Retrieve a service and assert its type."""
        service = self.get(name)
        if not isinstance(service, expected_type):
            raise TypeError(
                f"Service '{name}' is {type(service).__name__}, "
                f"expected {expected_type.__name__}"
            )
        return service

    def has(self, name: str) -> bool:
        """Check if a service is registered."""
        return name in self._services

    def clear(self) -> None:
        """Clear all registered services (useful for testing)."""
        self._services.clear()

    def __repr__(self) -> str:
        return f"ServiceRegistry(services={list(self._services.keys())})"


# Module-level singleton
registry = ServiceRegistry()
