"""Audio subsystem configuration (virtual mode defaults)."""

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class AudioConfig:
    """Audio processing parameters — virtual mode defaults."""

    sample_rate: int = 16000
    channels: int = 1
    chunk_size: int = 1024
    vad_threshold: float = 0.5
    silence_duration_ms: int = 700
    wakeword: str = "hey surya"
    supported_languages: List[str] = field(
        default_factory=lambda: ["en-IN", "en-US", "en-GB"]
    )

    # Virtual mode: STT/TTS handled by browser Web Speech API
    virtual_mode: bool = True
