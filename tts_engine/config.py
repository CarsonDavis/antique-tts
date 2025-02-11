# tts_engine/config.py
from pydantic import BaseModel, Field
from typing import Literal, ClassVar, Dict, Type
from pathlib import Path


class BaseConfig(BaseModel):
    """Base for all configs with CLI arg handling"""

    @classmethod
    def from_cli_args(cls, args: dict):
        """Create config from CLI arguments"""
        # Only include args that were explicitly set and match our fields
        config_values = {
            k: v for k, v in args.items() if k in cls.model_fields and v is not None
        }
        return cls(**config_values)


class TTSEngineConfig(BaseConfig):
    """Base configuration for all TTS engines"""

    engine_name: str = Field(..., frozen=True)
    cost_per_char: float = Field(default=0.0, description="Cost per character in USD")


class KokoroConfig(TTSEngineConfig):
    engine_name: Literal["kokoro"] = "kokoro"
    lang_code: str = Field(default="a", description="Language code for synthesis")
    speed: float = Field(default=1.0, description="Speech speed multiplier")
    voice: str = Field(default="am_michael", description="Voice model to use")
    cost_per_char: float = Field(default=0.0, description="Cost per character in USD")


class OpenAIConfig(TTSEngineConfig):
    engine_name: Literal["openai"] = "openai"
    model: str = Field(default="tts-1-hd", description="OpenAI TTS model to use")
    voice: str = Field(default="alloy", description="Voice to use for synthesis")
    response_format: str = Field(default="wav", description="Audio format for output")
    cost_per_char: float = Field(
        default=0.000015, description="Cost per character in USD"
    )


class TTSConfig(BaseConfig):
    """Main configuration supporting multiple engines"""

    engine_config: TTSEngineConfig
    output_dir: Path = Field(
        default=Path("output"), description="Output directory for audio files"
    )
    chunk_size: int = Field(default=4000, description="Maximum characters per chunk")
    max_workers: int = Field(default=4, description="Number of parallel workers")

    # Map engine types to their config classes
    ENGINE_CONFIGS: ClassVar[Dict[str, Type[TTSEngineConfig]]] = {
        "kokoro": KokoroConfig,
        "openai": OpenAIConfig,
    }

    @classmethod
    def create(cls, engine_name: str, cli_args: dict):
        """Factory method to create appropriate config"""
        if engine_name not in cls.ENGINE_CONFIGS:
            raise ValueError(f"Unsupported engine: {engine_name}")

        # Create engine config from CLI args
        engine_config = cls.ENGINE_CONFIGS[engine_name].from_cli_args(cli_args)

        # Use the same pattern for the main config
        return cls.from_cli_args(cli_args | {"engine_config": engine_config})
