"""Panda3D Camera Controller — Orbiting 3D camera with mouse tracking.

Positions camera to view the 3D robot and handles smooth rotation.
"""

from __future__ import annotations

import math
from panda3d.core import LVector3, NodePath


class CameraController:
    """Controls the main camera position and orbiting motion in Panda3D."""

    def __init__(self, camera_node: NodePath) -> None:
        self.camera = camera_node
        self.distance = 4.5
        self.pitch = -5.0
        self.heading = 0.0
        self.target = LVector3(0, 0, 0.2)
        self.update_camera()

    def update_camera((self)) -> None:
        """Calculate camera position based on spherical coordinates."""
        rad_h = math.radians(self.heading)
        rad_p = math.radians(self.pitch)

        x = self.target.get_x() + self.distance * math.sin(rad_h) * math.cos(rad_p)
        y = self.target.get_y() - self.distance * math.cos(rad_h) * math.cos(rad_p)
        z = self.target.get_z() + self.distance * math.sin(rad_p)

        self.camera.set_pos(x, y, z)
        self.camera.look_at(self.target)

    def orbit(self, delta_heading: float, delta_pitch: float) -> None:
        """Orbit the camera by angle deltas."""
        self.heading += delta_heading
        self.pitch = max(-45.0, min(45.0, self.pitch + delta_pitch))
        self.update_camera()
