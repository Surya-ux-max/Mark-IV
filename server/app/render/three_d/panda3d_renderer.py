"""Panda3D Renderer Application — Main ShowBase application & Event Bus integration.

Main entry point for native 3D Panda3D rendering:
- Listens to EventBus events (`ROBOT_STATE_CHANGED`, `ANIMATION_REQUESTED`, `EMOTION_CHANGED`)
- Updates 3D robot joint poses, camera, lighting, and procedural gestures in real time
- Can run windowed or offscreen for headless AI vision training
"""

from __future__ import annotations

import asyncio
from typing import Any, Optional

from app.core.logging import get_logger
from app.events.event_bus import event_bus
from app.events.event_types import EventType
from app.render.3d.animation_interpolator import AnimationInterpolator
from app.render.3d.camera_controller import CameraController
from app.render.3d.lighting_setup import LightingSetup
from app.render.3d.robot_mesh_builder import RobotMeshBuilder

try:
    from direct.showbase.ShowBase import ShowBase
    PANDA3D_AVAILABLE = True
except ImportError:
    PANDA3D_AVAILABLE = False
    ShowBase = object  # type: ignore

logger = get_logger(__name__)


class Panda3DRenderer(ShowBase if PANDA3D_AVAILABLE else object):
    """Panda3D 3D Robot Renderer Application."""

    def __init__(self, windowed: bool = True) -> None:
        if not PANDA3D_AVAILABLE:
            logger.warning("panda3d_not_installed")
            return

        # Initialize Panda3D ShowBase window
        super().__init__(windowType="no_window" if not windowed else "normal")

        if windowed:
            self.win.set_title("SurveX CSE Brain — 3D Panda3D Renderer")
            self.win.set_size(800, 600)

        self.set_background_color(0.02, 0.04, 0.08, 1.0)

        # Build 3D mesh, camera, and lighting
        self.builder = RobotMeshBuilder(self.render)
        self.lighting = LightingSetup(self.render)
        self.camera_ctrl = CameraController(self.camera)
        self.interpolator = AnimationInterpolator(self.builder.nodes)

        # Register step task in Panda3D task manager
        self.task_mgr.add(self._update_task, "panda3d_render_update")
        logger.info("panda3d_renderer_initialized")

    def _update_task(self, task) -> int:
        """Panda3D per-frame update loop."""
        dt = globalClock.get_dt()  # type: ignore[name-defined]
        self.interpolator.update(dt)

        # Idle floating animation for robot root node
        t = globalClock.get_frame_time()  # type: ignore[name-defined]
        if "root" in self.builder.nodes:
            float_y = 0.05 * (1.0 + 0.1 * dt)
            self.builder.nodes["root"].set_z(0.02 * (1 + 0.2 * (t % 3.0)))

        return task.cont  # type: ignore[name-defined]

    # ── Event Subscriptions ───────────────────────────────────────────────────

    async def on_robot_state_changed(self, event_type: str, payload: Any) -> None:
        """Handle state change — update point light and pose."""
        new_state = payload.get("new_state", "IDLE")
        self.lighting.set_state_color(new_state)

        if new_state == "GREETING":
            # Right arm wave
            self.interpolator.set_target_rotation("r_shoulder", (0, 75, 0))
            self.interpolator.set_target_rotation("r_elbow", (0, 25, 0))
        elif new_state == "THINKING":
            # Head tilt + right hand to chin
            self.interpolator.set_target_rotation("head", (-12, 10, 0))
            self.interpolator.set_target_rotation("r_shoulder", (0, 50, 0))
            self.interpolator.set_target_rotation("r_elbow", (0, 85, 0))
        elif new_state == "SLEEPING":
            # Head down, arms at sides
            self.interpolator.set_target_rotation("head", (0, -20, 0))
            self.interpolator.set_target_rotation("r_shoulder", (0, 0, 0))
            self.interpolator.set_target_rotation("l_shoulder", (0, 0, 0))
        else:
            # Standby / Idle pose
            self.interpolator.set_target_rotation("head", (0, 0, 0))
            self.interpolator.set_target_rotation("r_shoulder", (0, 10, 0))
            self.interpolator.set_target_rotation("l_shoulder", (0, -10, 0))
            self.interpolator.set_target_rotation("r_elbow", (0, 0, 0))
            self.interpolator.set_target_rotation("l_elbow", (0, 0, 0))

    async def on_animation_requested(self, event_type: str, payload: Any) -> None:
        """Handle animation cue requests."""
        anim = payload.get("animation", "").upper()
        if "WAVE" in anim:
            self.interpolator.set_target_rotation("r_shoulder", (0, 80, 0))
            self.interpolator.set_target_rotation("r_elbow", (0, 20, 0))
        elif "CELEBRAT" in anim:
            self.interpolator.set_target_rotation("r_shoulder", (0, 130, 0))
            self.interpolator.set_target_rotation("l_shoulder", (0, 130, 0))
