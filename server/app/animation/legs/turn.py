"""Turn animations — left and right body turns."""

from __future__ import annotations

from typing import List

from app.animation.legs.leg_pose import LegPose


def turn_left(degrees: float = 45.0) -> List[LegPose]:
    scale = degrees / 90.0
    return [
        LegPose(left_hip_angle=-20.0 * scale, right_hip_angle=10.0 * scale,
                left_knee_angle=10.0, body_lean=-5.0 * scale, duration_ms=400),
        LegPose(right_hip_angle=-5.0, body_lean=0.0, duration_ms=300),
        LegPose(duration_ms=300),  # settle
    ]


def turn_right(degrees: float = 45.0) -> List[LegPose]:
    scale = degrees / 90.0
    return [
        LegPose(left_hip_angle=10.0 * scale, right_hip_angle=-20.0 * scale,
                right_knee_angle=10.0, body_lean=5.0 * scale, duration_ms=400),
        LegPose(left_hip_angle=-5.0, body_lean=0.0, duration_ms=300),
        LegPose(duration_ms=300),
    ]
