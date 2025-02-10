# cli.py
import argparse
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from models.config import TTSConfig, VoiceConfig
from tts_engine.kokoro import KokoroEngine
from processors.chunker import TextChunker
from utils.file_manager import FileManager


def main():
    parser = argparse.ArgumentParser(description="Antique TTS Batch Processor")
    parser.add_argument("input_file", type=Path, help="Input text file path")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Output directory for audio files",
    )
    parser.add_argument(
        "--engine",
        choices=["kokoro", "openai"],
        default="kokoro",
        help="TTS engine to use",
    )
    parser.add_argument(
        "--chunk-size", type=int, default=4000, help="Maximum characters per chunk"
    )
    parser.add_argument(
        "--workers", type=int, default=4, help="Number of parallel synthesis workers"
    )

    args = parser.parse_args()

    config = TTSConfig(
        output_dir=args.output_dir,
        engine=args.engine,
        chunk_size=args.chunk_size,
        max_workers=args.workers,
    )

    # Process text
    chunker = TextChunker(config.chunk_size)
    with open(args.input_file) as f:
        chunks = chunker.process(f.read())

    # Initialize engine
    engine = (
        KokoroEngine(config.voice_settings)
        if config.engine == "kokoro"
        else OpenaiEngine(config)
    )

    # Create output directory
    FileManager.create_output_dir(config.output_dir)

    # Process chunks in parallel
    with ThreadPoolExecutor(max_workers=config.max_workers) as executor:
        futures = []
        for i, chunk in enumerate(chunks):
            output_path = config.output_dir / f"segment_{i:04d}.wav"
            futures.append(executor.submit(engine.synthesize, chunk, output_path))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            print(f"Generated: {result.output_file}")


if __name__ == "__main__":
    main()
