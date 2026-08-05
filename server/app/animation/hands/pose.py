"""HandPose — data model for a single arm/hand configuration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HandPose:
    """A single snapshot of hand/arm position.

    Angles are in degrees from the robot's neutral resting position.
    Positive = forward/up, Negative = backward/down.

    Hardware note: these map directly to servo angles on a physical robot.
    The renderer layer translates angles to CSS transforms for virtual mode.
    """

    # Arm angles (shoulder)
    left_arm_angle: float = 0.0    # -90 (down) to +180 (overhead)
    right_arm_angle: float = 0.0

    # Elbow angles
    left_elbow_angle: float = 0.0  # 0 (straight) to 90 (bent)
    right_elbow_angle: float = 0.0

    # Hand open/close
    left_open: bool = True
    right_open: bool = True

    # Wrist rotation
    left_wrist: float = 0.0        # -45 to +45
    right_wrist: float = 0.0

    # Duration to hold or reach this pose
    duration_ms: int = 300


# ── Predefined neutral poses ──────────────────────────────────────────────────

NEUTRAL_POSE = HandPose(
    left_arm_angle=0.0, right_arm_angle=0.0,
    left_elbow_angle=0.0, right_elbow_angle=0.0,
    left_open=True, right_open=True,
    duration_ms=400,
)

FOLD_POSE = HandPose(
    left_arm_angle=30.0, right_arm_angle=30.0,
    left_elbow_angle=60.0, right_elbow_angle=60.0,
    left_open=False, right_open=False,
    duration_ms=500,
)
