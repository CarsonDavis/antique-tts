# tts_engine/kokoro.py
from pathlib import Path
import soundfile as sf
from .base import TTSEngine, SynthesisResult
from models.config import VoiceConfig
from kokoro import KPipeline


class KokoroEngine(TTSEngine):
    def __init__(self, config: VoiceConfig):
        super().__init__(config)
        self.pipeline = KPipeline(lang_code=config.lang_code)

    def synthesize(self, text: str, output_path: Path) -> SynthesisResult:
        print(f"Starting synthesis for {len(text)} characters")  # Progress indicator
        try:
            generator = self.pipeline(
                text,
                voice=self.config.voice,
                speed=self.config.speed,
                split_pattern=r"",
            )

            results = []
            for i, (_, _, audio) in enumerate(generator):
                print(f"Processing chunk {i+1}")  # Chunk progress
                filename = output_path.with_name(f"{output_path.stem}_{i}.wav")
                sf.write(filename, audio, 24000)
                results.append(filename)

            return SynthesisResult(
                output_file=results[0] if len(results) == 1 else output_path.parent,
                character_count=len(text),
                processing_time=0.0,
            )
        except Exception as e:
            print(f"Synthesis failed: {str(e)}")
            raise
