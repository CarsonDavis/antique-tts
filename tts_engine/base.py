# tts_engine/base.py
from pathlib import Path
from pydantic import BaseModel
from tts_engine.config import TTSEngineConfig


class SynthesisResult(BaseModel):
    output_file: Path
    character_count: int


class TTSEngine:
    def __init__(self, config: TTSEngineConfig):
        self.config = config

    def synthesize(self, text: str, output_path: Path) -> SynthesisResult:
        """Core interface for all TTS implementations"""
        raise NotImplementedError
