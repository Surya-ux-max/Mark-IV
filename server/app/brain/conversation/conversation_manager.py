"""Conversation manager — the core brain orchestrating each user turn.

Flow per user message:
  1. Detect intent
  2. Retrieve relevant knowledge (RAG)
  3. Build system prompt with context
  4. Get conversation history
  5. Call Groq LLM
  6. Clean response
  7. Store turn in history
  8. Return response + metadata
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from app.brain.decision_engine.intent_detector import detect_intent
from app.brain.reasoning.prompt_builder import build_system_prompt
from app.brain.reasoning.response_parser import clean_response
from app.config.constants import IntentType
from app.config.settings import Settings
from app.core.logging import get_logger
from app.memory.history.history_manager import HistoryManager
from app.memory.rag.rag_engine import RAGEngine
from app.models.messages import ConversationTurn
from app.services.llm.llm_service import LLMService

logger = get_logger(__name__)


@dataclass
class TurnResult:
    """Result of processing a single user turn."""

    response_text: str
    intent: str
    knowledge_sources: List[str] = field(default_factory=list)
    emotion_hint: str = "NEUTRAL"


class ConversationManager:
    """Orchestrates a full user→robot conversation turn."""

    def __init__(
        self,
        llm_service: LLMService,
        rag_engine: RAGEngine,
        history_manager: HistoryManager,
        settings: Settings,
    ) -> None:
        self._llm = llm_service
        self._rag = rag_engine
        self._history = history_manager
        self._settings = settings

    async def process(self, user_text: str, session_id: str) -> TurnResult:
        """Process a user message and return the robot's response."""

        logger.info("conversation_turn_start", session_id=session_id, text=user_text[:80])

        # ── 1. Detect intent ───────────────────────────────────────────────────
        intent = detect_intent(user_text)
        logger.debug("intent_detected", intent=intent, session=session_id)

        # ── 2. Retrieve knowledge context ─────────────────────────────────────
        context_block, sources = await self._rag.get_context(user_text)

        # ── 3. Build system prompt ────────────────────────────────────────────
        system_prompt = build_system_prompt(
            settings=self._settings,
            context_block=context_block,
        )

        # ── 4. Get conversation history ───────────────────────────────────────
        history_messages = self._history.get_groq_messages(session_id)

        # ── 5. Add current user message ───────────────────────────────────────
        messages = history_messages + [{"role": "user", "content": user_text}]

        # ── 6. Call Groq LLM ──────────────────────────────────────────────────
        raw_response = await self._llm.generate(
            system_prompt=system_prompt,
            messages=messages,
        )

        # ── 7. Clean response ─────────────────────────────────────────────────
        response_text = clean_response(raw_response)

        # ── 8. Store turn in history ──────────────────────────────────────────
        turn = ConversationTurn(
            user_text=user_text,
            robot_text=response_text,
            intent=intent.value,
            knowledge_sources=sources,
        )
        self._history.add_turn(session_id, turn)

        # ── 9. Determine emotion hint ─────────────────────────────────────────
        emotion_hint = self._get_emotion_hint(intent)

        logger.info(
            "conversation_turn_complete",
            session_id=session_id,
            intent=intent,
            sources=sources,
            response_length=len(response_text),
        )

        return TurnResult(
            response_text=response_text,
            intent=intent.value,
            knowledge_sources=sources,
            emotion_hint=emotion_hint,
        )

    def _get_emotion_hint(self, intent: IntentType) -> str:
        """Map intent to a suggested emotion for the emotion engine."""
        mapping = {
            IntentType.GREETING: "HAPPY",
            IntentType.FAREWELL: "CALM",
            IntentType.KNOWLEDGE_QUERY: "CURIOUS",
            IntentType.QUESTION: "CURIOUS",
            IntentType.CHITCHAT: "HAPPY",
            IntentType.COMMAND: "NEUTRAL",
            IntentType.UNKNOWN: "NEUTRAL",
        }
        return mapping.get(intent, "NEUTRAL")
