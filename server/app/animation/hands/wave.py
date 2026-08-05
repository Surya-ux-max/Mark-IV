"""Wave gesture — friendly right-hand wave animation.

Keyframe sequence:
  1. Raise right arm to 90°
  2. Wrist oscillate left/right × 3
  3. Return to neutral

Usage:
  frames = wave()
  await hand_controller.play(frames)
"""

from __future__ import annotations

from typing import List

from app.animation.hands.pose import HandPose


def wave(loops: int = 3, intensity: float = 1.0) -> List[HandPose]:
    """Build a right-hand wave gesture keyframe list."""
    scale = max(0.3, min(1.0, intensity))
    arm_angle = 90.0 * scale
    wrist_range = 35.0 * scale

    frames: List[HandPose] = [
        # Raise arm
        HandPose(right_arm_angle=arm_angle, right_elbow_angle=15.0, right_open=True, duration_ms=350),
    ]
    # Wrist oscillation
    for _ in range(loops):
        frames.append(HandPose(right_arm_angle=arm_angle, right_wrist=-wrist_range, right_open=True, duration_ms=180))
        frames.append(HandPose(right_arm_angle=arm_angle, right_wrist=+wrist_range, right_open=True, duration_ms=180))

    # Return to neutral
    frames.append(HandPose(right_arm_angle=0.0, right_elbow_angle=0.0, right_wrist=0.0, right_open=True, duration_ms=400))
    return frames
