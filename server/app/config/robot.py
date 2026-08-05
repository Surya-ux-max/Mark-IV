"""Robot personality and behavior configuration."""

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class RobotConfig:
    """Robot behavior and personality parameters."""

    name: str = "Surya"
    department: str = "Computer Science and Engineering"
    institution: str = "Department of CSE"
    default_language: str = "en-IN"
    speaking_rate: float = 1.0  # multiplier (1.0 = normal)
    response_timeout_seconds: float = 30.0
    idle_timeout_seconds: float = 120.0  # go to observing after 2 min
    greeting_phrases: List[str] = field(
        default_factory=lambda: [
            "Hello! I'm Surya, your CSE department assistant. How can I help you today?",
            "Hi there! Welcome. I'm Surya. What would you like to know?",
            "Good to see you! I'm Surya. Feel free to ask me anything about our CSE program.",
        ]
    )
    sleep_phrases: List[str] = field(
        default_factory=lambda: [
            "Going to sleep now. Press the button to wake me up!",
            "Entering sleep mode. See you soon!",
        ]
    )
    wake_phrases: List[str] = field(
        default_factory=lambda: [
            "I'm awake! How can I help you?",
            "Hello! Ready to assist you.",
        ]
    )
