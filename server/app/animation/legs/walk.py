"""Walk animation — bipedal walk cycle keyframes."""

from __future__ import annotations

from typing import List

from app.animation.legs.leg_pose import LegPose


def walk_cycle(steps: int = 4, speed: float = 1.0) -> List[LegPose]:
    """Generate a walk cycle with the given number of steps."""
    step_ms = int(500 / speed)
    frames: List[LegPose] = []
    for i in range(steps):
        # Left step
        frames.append(LegPose(
            left_hip_angle=25.0,  right_hip_angle=-15.0,
            left_knee_angle=15.0, right_knee_angle=5.0,
            body_lean=5.0, duration_ms=step_ms,
        ))
        # Right step
        frames.append(LegPose(
            left_hip_angle=-15.0, right_hip_angle=25.0,
            left_knee_angle=5.0,  right_knee_angle=15.0,
            body_lean=5.0, duration_ms=step_ms,
        ))
    # Return to stance
    frames.append(LegPose(duration_ms=400))
    return frames
