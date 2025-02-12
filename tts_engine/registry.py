# tts_engine/registry.py
from .kokoro import KokoroEngine
from .openai import OpenAIEngine
from .edgetts import EdgeTTSEngine
from .config import KokoroConfig, OpenAIConfig, EdgeTTSConfig

TTS_REGISTRY = {
    "kokoro": {
        "engine": KokoroEngine,
        "config": KokoroConfig,
    },
    "openai": {
        "engine": OpenAIEngine,
        "config": OpenAIConfig,
    },
    "edge-tts": {
        "engine": EdgeTTSEngine,
        "config": EdgeTTSConfig,
    },
}
