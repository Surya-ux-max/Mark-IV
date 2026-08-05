"""Custom exception hierarchy for SurveX Virtual Robot."""


class RobotException(Exception):
    """Base exception for all robot-related errors."""

    def __init__(self, message: str, code: str = "ROBOT_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(code={self.code!r}, message={self.message!r})"


class LLMException(RobotException):
    """Raised when the LLM service fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="LLM_ERROR")


class KnowledgeException(RobotException):
    """Raised when knowledge base loading or retrieval fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="KNOWLEDGE_ERROR")


class WebSocketException(RobotException):
    """Raised on WebSocket protocol or connection errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="WEBSOCKET_ERROR")


class StateTransitionException(RobotException):
    """Raised when an invalid robot state transition is attempted."""

    def __init__(self, from_state: str, to_state: str) -> None:
        super().__init__(
            f"Invalid transition: {from_state} → {to_state}",
            code="INVALID_STATE_TRANSITION",
        )
        self.from_state = from_state
        self.to_state = to_state


class EventBusException(RobotException):
    """Raised on event bus errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="EVENT_BUS_ERROR")


class ConfigurationException(RobotException):
    """Raised on configuration validation errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="CONFIG_ERROR")
