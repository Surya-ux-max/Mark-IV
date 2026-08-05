"""LegPose — data model for lower-body position.

Hardware note: maps to hip/knee servo angles on a physical humanoid.
Virtual mode: translates to CSS transforms for the frontend.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LegPose:
    """A single snapshot of leg/foot configuration.

    Angles in degrees from neutral upright stance.
    """
    left_hip_angle:  float = 0.0   # forward/back swing
    right_hip_angle: float = 0.0
    left_knee_angle: float = 0.0   # bend 0–90
    right_knee_angle: float = 0.0
    left_ankle_angle: float = 0.0  # tilt
    right_ankle_angle: float = 0.0
    body_lean: float = 0.0         # forward lean degrees
    duration_ms: int = 400


STANCE_POSE = LegPose(
    left_hip_angle=0.0, right_hip_angle=0.0,
    left_knee_angle=5.0, right_knee_angle=5.0,
    body_lean=0.0, duration_ms=400,
)
