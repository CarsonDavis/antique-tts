# models/config.py
from pathlib import Path
from typing import Literal
from pydantic import BaseModel


class VoiceConfig(BaseModel):
    lang_code: str = "a"
    speed: float = 1.0
    voice: str = "am_michael"


class TTSConfig(BaseModel):
    output_dir: Path
    engine: Literal["kokoro", "openai"] = "kokoro"
    chunk_size: int = 4000
    max_workers: int = 4
    voice_settings: VoiceConfig = VoiceConfig()
    speed: float = 1.0
    language: str = "en-US"
