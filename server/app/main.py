"""FastAPI application factory — full enterprise robot platform startup.

Startup order:
  1. Logging
  2. RAG Engine
  3. LLM Service
  4. History Manager + Conversation Manager
  5. Emotion Engine (full 18-emotion)
  6. Animation subsystems: Face, Hand, Leg, Timeline
  7. Behavior Manager
  8. Robot FSM + Controller
  9. WebSocket Manager
  10. Wire all event subscriptions
  11. Register services
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.animation.face.face_controller import FaceController
from app.animation.hands.hand_controller import HandController
from app.animation.legs.leg_controller import LegController
from app.animation.timeline.timeline_controller import TimelineController
from app.api.routes import chat, health, knowledge, robot
from app.api.websocket.ws_handler import handle_websocket
from app.api.websocket.ws_manager import WSManager
from app.brain.conversation.conversation_manager import ConversationManager
from app.config.settings import get_settings
from app.core.logging import configure_logging, get_logger
from app.core.registry import registry
from app.emotion.engine.emotion_engine import EmotionEngine
from app.events.dispatcher import setup_event_subscriptions
from app.memory.history.history_manager import HistoryManager
from app.memory.rag.rag_engine import RAGEngine
from app.robot.behaviors.behavior_manager import BehaviorManager
from app.robot.controller.robot_controller import RobotController
from app.robot.state_machine.state_machine import RobotStateMachine
from app.services.llm.llm_factory import create_groq_client
from app.services.llm.llm_service import LLMService

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()

    # ── 1. Logging ────────────────────────────────────────────────────────────
    configure_logging(log_level=settings.log_level)
    logger.info("survex_robot_starting", robot_name=settings.robot_name)

    # ── 2. RAG Engine ─────────────────────────────────────────────────────────
    rag_engine = RAGEngine(knowledge_path=settings.knowledge_path, top_k=settings.top_k_docs)
    await rag_engine.initialize()

    # ── 3. LLM Service ────────────────────────────────────────────────────────
    groq_client = create_groq_client(settings)
    llm_service = LLMService(client=groq_client)
    await llm_service.initialize()

    # ── 4. Memory + Conversation ──────────────────────────────────────────────
    history_manager = HistoryManager(max_turns=settings.max_history_turns)
    conversation_manager = ConversationManager(
        llm_service=llm_service,
        rag_engine=rag_engine,
        history_manager=history_manager,
        settings=settings,
    )

    # ── 5. Emotion Engine ─────────────────────────────────────────────────────
    emotion_engine = EmotionEngine()
    await emotion_engine.initialize()

    # ── 6. Animation subsystems ───────────────────────────────────────────────
    hand_controller   = HandController()
    leg_controller    = LegController()
    face_controller   = FaceController()
    timeline_ctrl     = TimelineController()

    # ── 7. Behavior Manager ───────────────────────────────────────────────────
    behavior_manager = BehaviorManager(hand_controller, leg_controller)

    # ── 8. Robot FSM + Controller ─────────────────────────────────────────────
    state_machine    = RobotStateMachine()
    robot_controller = RobotController(
        state_machine=state_machine,
        conversation_manager=conversation_manager,
    )

    # ── 9. WebSocket Manager ──────────────────────────────────────────────────
    ws_manager = WSManager()

    # Wire timeline broadcast to WSManager so it can push directly
    timeline_ctrl.set_broadcast(ws_manager.broadcast)

    # ── 10. Event Subscriptions ───────────────────────────────────────────────
    await setup_event_subscriptions(
        robot_controller=robot_controller,
        ws_manager=ws_manager,
        emotion_engine=emotion_engine,
        face_controller=face_controller,
        timeline_controller=timeline_ctrl,
        behavior_manager=behavior_manager,
    )

    # ── 11. Service Registry ──────────────────────────────────────────────────
    registry.register("rag_engine",           rag_engine)
    registry.register("llm_service",          llm_service)
    registry.register("history_manager",      history_manager)
    registry.register("conversation_manager", conversation_manager)
    registry.register("emotion_engine",       emotion_engine)
    registry.register("hand_controller",      hand_controller)
    registry.register("leg_controller",       leg_controller)
    registry.register("face_controller",      face_controller)
    registry.register("timeline_controller",  timeline_ctrl)
    registry.register("behavior_manager",     behavior_manager)
    registry.register("robot_controller",     robot_controller)
    registry.register("ws_manager",           ws_manager)
    registry.register("settings",            settings)

    app.state.ws_manager       = ws_manager
    app.state.robot_controller = robot_controller
    app.state.settings         = settings

    logger.info("survex_robot_ready", state=state_machine.current_state)
    yield

    # ── Shutdown ──────────────────────────────────────────────────────────────
    logger.info("survex_robot_shutting_down")
    await emotion_engine.shutdown()
    await llm_service.shutdown()
    await rag_engine.shutdown()
    registry.clear()
    logger.info("survex_robot_stopped")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="SurveX Virtual Robot API",
        description="Real-time AI-powered virtual robot — CSE Department",
        version="0.2.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(robot.router)
    app.include_router(chat.router)
    app.include_router(knowledge.router)

    @app.websocket("/ws")
    async def websocket_endpoint(ws: WebSocket) -> None:
        await handle_websocket(
            websocket=ws,
            ws_manager=app.state.ws_manager,
            robot_controller=app.state.robot_controller,
            settings=app.state.settings,
        )

    return app


app = create_app()
