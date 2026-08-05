"""FastAPI dependency providers for all services."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from app.core.registry import registry


def get_robot_controller():
    return registry.get("robot_controller")


def get_ws_manager():
    return registry.get("ws_manager")


def get_conversation_manager():
    return registry.get("conversation_manager")


def get_rag_engine():
    return registry.get("rag_engine")


def get_llm_service():
    return registry.get("llm_service")
