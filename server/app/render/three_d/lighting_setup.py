"""Panda3D Lighting Setup — Studio lights + State-reactive ambient point lights.

Manages 3D lighting for the Panda3D robot stage:
- Key light & Fill light for studio depth
- Dynamic point light whose color shifts according to robot state
"""

from __future__ import annotations

from typing import Dict
from panda3d.core import AmbientLight, LColor, NodePath, PointLight


STATE_LIGHT_COLORS: Dict[str, LColor] = {
    "SLEEPING":  LColor(0.2, 0.3, 0.6, 1.0),
    "IDLE":      LColor(0.0, 0.9, 1.0, 1.0),
    "LISTENING": LColor(0.3, 0.6, 1.0, 1.0),
    "THINKING":  LColor(1.0, 0.7, 0.0, 1.0),
    "SPEAKING":  LColor(0.0, 1.0, 0.6, 1.0),
    "GREETING":  LColor(0.8, 0.4, 1.0, 1.0),
    "OBSERVING": LColor(0.0, 0.9, 1.0, 1.0),
    "ERROR":     LColor(1.0, 0.2, 0.3, 1.0),
}


class LightingSetup:
    """Manages studio lighting and state light transitions in Panda3D."""

    def __init__(self, render_root: NodePath) -> None:
        self.root = render_root
        self.state_light = PointLight("state_point_light")
        self.state_light_node: NodePath = NodePath()
        self._setup_lights()

    def _setup_lights(self) -> None:
        # Ambient studio light
        ambient = AmbientLight("ambient_light")
        ambient.set_color(LColor(0.35, 0.38, 0.42, 1.0))
        ambient_np = self.root.attach_new_node(ambient)
        self.root.set_light(ambient_np)

        # Key Directional Point light
        key_light = PointLight("key_light")
        key_light.set_color(LColor(0.9, 0.95, 1.0, 1.0))
        key_np = self.root.attach_new_node(key_light)
        key_np.set_pos(4.0, -6.0, 6.0)
        self.root.set_light(key_np)

        # Reactive State light
        self.state_light.set_color(STATE_LIGHT_COLORS["IDLE"])
        self.state_light_node = self.root.attach_new_node(self.state_light)
        self.state_light_node.set_pos(0, -3.0, 1.0)
        self.root.set_light(self.state_light_node)

    def set_state_color(self, state_name: str) -> None:
        """Update point light color to match robot state."""
        color = STATE_LIGHT_COLORS.get(state_name.upper(), STATE_LIGHT_COLORS["IDLE"])
        self.state_light.set_color(color)
