"""Robot FSM orchestrator — manages all state transitions.

The state machine holds the current state, receives events from the
event bus via RobotController, transitions between states, and calls
on_enter/on_exit hooks.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from app.config.constants import RobotState
from app.core.exceptions import StateTransitionException
from app.core.logging import get_logger
from app.events.publishers import RobotPublisher
from app.robot.state_machine.base_state import BaseState
from app.robot.state_machine.error_state import ErrorState
from app.robot.state_machine.greeting_state import GreetingState
from app.robot.state_machine.idle_state import IdleState
from app.robot.state_machine.listening_state import ListeningState
from app.robot.state_machine.observing_state import ObservingState
from app.robot.state_machine.sleeping_state import SleepingState
from app.robot.state_machine.speaking_state import SpeakingState
from app.robot.state_machine.thinking_state import ThinkingState

logger = get_logger(__name__)


class RobotStateMachine:
    """Finite state machine for robot lifecycle management."""

    def __init__(self) -> None:
        self._states: Dict[str, BaseState] = {
            RobotState.SLEEPING: SleepingState(),
            RobotState.GREETING: GreetingState(),
            RobotState.IDLE: IdleState(),
            RobotState.LISTENING: ListeningState(),
            RobotState.THINKING: ThinkingState(),
            RobotState.SPEAKING: SpeakingState(),
            RobotState.OBSERVING: ObservingState(),
            RobotState.ERROR: ErrorState(),
        }
        self._current: BaseState = self._states[RobotState.SLEEPING]
        self._context: Any = None

    def set_context(self, context: Any) -> None:
        """Inject shared context (e.g., session data) available to states."""
        self._context = context

    @property
    def current_state(self) -> RobotState:
        return self._current.state_id

    @property
    def is_awake(self) -> bool:
        return self._current.state_id != RobotState.SLEEPING

    async def dispatch(self, event_type: str, payload: Any = None) -> bool:
        """Dispatch an event to the current state.

        Returns True if a state transition occurred.
        """
        next_state_id = await self._current.handle_event(
            event_type, payload or {}, self._context
        )

        if next_state_id and next_state_id != self._current.state_id:
            await self._transition(next_state_id)
            return True

        return False

    async def _transition(self, next_state_id: str) -> None:
        """Execute a state transition with on_exit / on_enter hooks."""
        if next_state_id not in self._states:
            raise StateTransitionException(
                self._current.state_id, next_state_id
            )

        previous = self._current.state_id
        next_state = self._states[next_state_id]

        logger.info(
            "state_transition",
            from_state=previous,
            to_state=next_state_id,
        )

        await self._current.on_exit(self._context)
        self._current = next_state
        await self._current.on_enter(self._context)

        await RobotPublisher.state_changed(previous, next_state_id)
