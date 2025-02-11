import asyncio
from pathlib import Path
from edge_tts import Communicate
from .base import TTSEngine, SynthesisResult
from .config import EdgeTTSConfig


class EdgeTTSEngine(TTSEngine):
    """Edge TTS engine implementation"""
    
    def __init__(self, config: EdgeTTSConfig):
        super().__init__(config)
        
    async def _synthesize_async(self, text: str, output_path: Path) -> None:
        """Internal async method to perform TTS synthesis"""
        communicate = Communicate(text, self.config.voice)
        
        with open(output_path, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])

    def synthesize(
        self, text: str, output_path: Path, chunk_index: int = 1
    ) -> SynthesisResult:
        """Synthesize text to speech using Edge TTS"""
        print(f"📦 Processing text chunk {chunk_index} ({len(text)} characters)")
        
        try:
            print(f"   🔊 Generating audio with Edge TTS...")
            asyncio.run(self._synthesize_async(text, output_path))
            print(f"   💾 Saved audio to {output_path}")
            
            return SynthesisResult(
                output_file=output_path,
                character_count=len(text)
            )
            
        except Exception as e:
            print(f"   ❌ Error processing chunk {chunk_index}: {str(e)}")
            raise
