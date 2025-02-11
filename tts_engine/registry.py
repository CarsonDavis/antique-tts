# tts_engine/registry.py
from .kokoro import KokoroEngine
from .openai import OpenAIEngine
from .config import KokoroConfig, OpenAIConfig

TTS_REGISTRY = {
    "kokoro": {
        "engine": KokoroEngine,
        "config": KokoroConfig,
    },
    "openai": {
        "engine": OpenAIEngine,
        "config": OpenAIConfig,
    },
}
