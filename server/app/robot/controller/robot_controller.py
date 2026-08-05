"""Robot controller — top-level orchestrator that ties all subsystems together.

Receives events from the event bus, dispatches them to the state machine,
and invokes the conversation manager for user messages.
"""

from __future__ import annotations

from typing import Any

from app.brain.conversation.conversation_manager import ConversationManager
from app.config.constants import RobotState
from app.core.logging import get_logger
from app.events.event_types import EventType
from app.events.publishers import LLMPublisher, RobotPublisher
from app.robot.state_machine.state_machine import RobotStateMachine

logger = get_logger(__name__)


class RobotController:
    """Top-level robot orchestrator. Wires events → state machine → brain."""

    def __init__(
        self,
        state_machine: RobotStateMachine,
        conversation_manager: ConversationManager,
    ) -> None:
        self._fsm = state_machine
        self._conversation = conversation_manager

    # ── Event handlers (subscribed in dispatcher.py) ──────────────────────────

    async def on_user_message(self, event_type: str, payload: Any) -> None:
        """Handle incoming user text message."""
        text: str = payload.get("text", "").strip()
        session_id: str = payload.get("session_id", "default")

        if not text:
            return

        if not self._fsm.is_awake:
            logger.debug("robot_sleeping_ignored_message", text=text[:40])
            return

        # Transition to THINKING
        await self._fsm.dispatch(EventType.USER_MESSAGE_RECEIVED, payload)
        await RobotPublisher.started_thinking(session_id)

        try:
            result = await self._conversation.process(text, session_id)

            # Transition to SPEAKING via LLM_RESPONSE_READY event
            await LLMPublisher.response_ready(
                text=result.response_text,
                session_id=session_id,
                sources=result.knowledge_sources,
            )
            await self._fsm.dispatch(EventType.LLM_RESPONSE_READY, {"text": result.response_text})

            await RobotPublisher.started_speaking(result.response_text, session_id)

        except Exception as exc:
            logger.error("conversation_error", error=str(exc), session=session_id)
            await self._fsm.dispatch(EventType.SYSTEM_ERROR, {"error": str(exc)})

    async def on_command(self, event_type: str, payload: Any) -> None:
        """Handle robot commands (WAKE_UP, SLEEP, RESET, etc.)."""
        command = payload.get("command", "")
        logger.info("command_received", command=command)

        if command == "WAKE_UP":
            await RobotPublisher.woke_up()
        elif command == "SLEEP":
            await RobotPublisher.went_to_sleep()

        await self._fsm.dispatch(EventType.COMMAND_RECEIVED, payload)

    async def on_face_detected(self, event_type: str, payload: Any) -> None:
        if self._fsm.is_awake:
            await self._fsm.dispatch(EventType.FACE_DETECTED, payload)

    async def on_face_lost(self, event_type: str, payload: Any) -> None:
        if self._fsm.current_state == RobotState.OBSERVING:
            await self._fsm.dispatch(EventType.FACE_LOST, payload)

    async def notify_speaking_done(self, session_id: str) -> None:
        """Called by WSManager when client signals TTS is complete."""
        await RobotPublisher.stopped_speaking(session_id)
        await self._fsm.dispatch(EventType.ROBOT_STOPPED_SPEAKING, {"session_id": session_id})

    @property
    def current_state(self) -> str:
        return self._fsm.current_state.value

    @property
    def is_awake(self) -> bool:
        return self._fsm.is_awake
