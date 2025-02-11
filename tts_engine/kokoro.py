# tts_engine/kokoro.py
from pathlib import Path
import soundfile as sf
from .base import TTSEngine, SynthesisResult
from tts_engine.config import KokoroConfig
from kokoro import KPipeline
from utils.file_manager import FileManager
from pathlib import Path
from kokoro import KPipeline


class KokoroEngine(TTSEngine):
    def __init__(self, config: KokoroConfig):
        super().__init__(config)

        self.pipeline = KPipeline(lang_code=config.lang_code)

    def synthesize(
        self, text: str, output_path: Path, chunk_index: int = 1
    ) -> SynthesisResult:
        print(f"📦 Processing text chunk {chunk_index} ({len(text)} characters)")
        try:
            generator = self.pipeline(
                text,
                voice=self.config.voice,
                speed=self.config.speed,
                split_pattern=r"",
            )
            results = []
            for segment_number, (_, _, audio) in enumerate(generator, start=1):
                print(f"   🔊 Audio segment {chunk_index}.{segment_number}")
                filename = output_path.with_name(
                    f"{output_path.stem}_s{segment_number:03d}.wav"
                )
                FileManager.safe_write_audio(filename, audio)
                results.append(filename)

            return SynthesisResult(
                output_file=results[0] if len(results) == 1 else output_path.parent,
                character_count=len(text),
                processing_time=0.0,
            )
        except Exception as e:
            print(f"Synthesis failed: {str(e)}")
            raise
