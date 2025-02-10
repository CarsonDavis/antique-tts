# tts_engine/base.py
from abc import ABC, abstractmethod
from pathlib import Path
from dataclasses import dataclass
from models.config import VoiceConfig


@dataclass
class SynthesisResult:
    output_file: Path
    character_count: int
    processing_time: float


class TTSEngine(ABC):
    def __init__(self, config: VoiceConfig):
        self.config = config

    @abstractmethod
    def synthesize(self, text: str, output_path: Path) -> SynthesisResult:
        """Convert text to speech and return metadata about the synthesis"""
        raise NotImplementedError
