"""Panda3D Animation Interpolator — Smooth joint angle interpolation.

Lerps 3D joint rotations for head, arms, legs between poses over time.
"""

from __future__ import annotations

from typing import Dict, Tuple
from panda3d.core import LVector3, NodePath


class AnimationInterpolator:
    """Smoothly lerps Panda3D node rotations for robot joints."""

    def __init__(self, nodes: Dict[str, NodePath]) -> None:
        self.nodes = nodes
        self._target_rotations: Dict[str, Tuple[float, float, float]] = {}

    def set_target_rotation(self, node_name: str, hpr: Tuple[float, float, float]) -> None:
        """Set target Heading, Pitch, Roll for a node."""
        if node_name in self.nodes:
            self._target_rotations[node_name] = hpr

    def update(self, dt: float, lerp_factor: float = 8.0) -> None:
        """Step interpolation toward target rotations."""
        for name, target_hpr in self._target_rotations.items():
            node = self.nodes.get(name)
            if not node:
                continue

            current_hpr = node.get_hpr()
            new_h = current_hpr.get_x() + (target_hpr[0] - current_hpr.get_x()) * dt * lerp_factor
            new_p = current_hpr.get_y() + (target_hpr[1] - current_hpr.get_y()) * dt * lerp_factor
            new_r = current_hpr.get_z() + (target_hpr[2] - current_hpr.get_z()) * dt * lerp_factor

            node.set_hpr(new_h, new_p, new_r)
