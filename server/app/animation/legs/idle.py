"""Idle leg animations — subtle weight shifts while standing."""

from __future__ import annotations

from typing import List

from app.animation.legs.leg_pose import LegPose, STANCE_POSE


def idle_sway() -> List[LegPose]:
    """Gentle weight shift left/right — natural standing idle."""
    return [
        STANCE_POSE,
        LegPose(left_hip_angle=3.0, right_hip_angle=-3.0, left_knee_angle=8.0, duration_ms=1500),
        STANCE_POSE,
        LegPose(left_hip_angle=-3.0, right_hip_angle=3.0, right_knee_angle=8.0, duration_ms=1500),
        STANCE_POSE,
    ]


def idle_bounce() -> List[LegPose]:
    """Excited idle — slight vertical bounce."""
    return [
        LegPose(left_knee_angle=12.0, right_knee_angle=12.0, duration_ms=300),
        LegPose(left_knee_angle=4.0,  right_knee_angle=4.0,  duration_ms=300),
        LegPose(left_knee_angle=12.0, right_knee_angle=12.0, duration_ms=300),
        LegPose(left_knee_angle=4.0,  right_knee_angle=4.0,  duration_ms=300),
        STANCE_POSE,
    ]
