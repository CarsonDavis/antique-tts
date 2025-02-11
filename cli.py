# cli.py
import argparse
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from tts_engine.config import TTSConfig, TTSEngineConfig
from tts_engine import OpenAIEngine, KokoroEngine
from utils import (
    TextChunker,
    FileManager,
    get_user_confirmation,
    calculate_cost,
    calculate_total_characters,
)


# Map engine types to their engine classes
ENGINE_CLASSES = {
    "kokoro": KokoroEngine,
    "openai": OpenAIEngine,
}


def create_arg_parser():
    parser = argparse.ArgumentParser(description="TTS Cli")

    # Add required input file argument
    parser.add_argument("input_file", type=Path, help="Input text file path")

    # Add engine selection argument
    parser.add_argument(
        "--engine",
        choices=list(TTSConfig.ENGINE_CONFIGS.keys()),
        default="kokoro",
        help="TTS engine to use",
    )

    # Add base TTSConfig arguments
    for field_name, field in TTSConfig.model_fields.items():
        if field_name != "engine_config":  # Skip the engine config field
            parser.add_argument(
                f"--{field_name.replace('_', '-')}",
                type=field.annotation,
                default=None,
                help=field.description,
            )

    # Create a dict of all unique engine-specific arguments
    engine_args = {}
    for engine_name, config_class in TTSConfig.ENGINE_CONFIGS.items():
        for field_name, field in config_class.model_fields.items():
            # Skip frozen fields and parent class fields
            if not field.frozen and field_name not in TTSEngineConfig.model_fields:
                if field_name not in engine_args:
                    engine_args[field_name] = {
                        "type": field.annotation,
                        "description": field.description,
                        "engines": [engine_name],
                    }
                else:
                    engine_args[field_name]["engines"].append(engine_name)

    # Add engine-specific arguments
    engine_group = parser.add_argument_group("Engine-specific options")
    for field_name, info in engine_args.items():
        engines_str = ", ".join(info["engines"])
        engine_group.add_argument(
            f"--{field_name.replace('_', '-')}",
            type=info["type"],
            default=None,
            help=f"({engines_str}) {info['description']}",
        )

    return parser


def main():
    parser = create_arg_parser()
    args = parser.parse_args()

    # Convert args to dict, only including non-None values
    cli_args = {k: v for k, v in vars(args).items() if v is not None}

    # Create config using factory method
    config = TTSConfig.create(args.engine, cli_args)

    # Read input text and calculate total characters
    with open(args.input_file) as f:
        input_text = f.read()

    total_chars = calculate_total_characters(input_text, config.chunk_size)

    # Calculate and confirm costs if necessary
    total_cost = calculate_cost(total_chars, config.engine_config.cost_per_char)

    if not get_user_confirmation(total_cost):
        print("Operation cancelled by user.")
        return

    # Create appropriate engine instance
    engine_class = ENGINE_CLASSES[config.engine_config.engine_name]
    engine = engine_class(config.engine_config)

    # Process text
    chunker = TextChunker(config.chunk_size)
    chunks = chunker.process(input_text)

    # Create output directory
    FileManager.create_output_dir(config.output_dir)

    # Process chunks in parallel
    with ThreadPoolExecutor(max_workers=config.max_workers) as executor:
        futures = [
            executor.submit(
                engine.synthesize,
                chunk,
                config.output_dir / f"output_chunk_{i+1:04d}.wav",
                chunk_index=i + 1,
            )
            for i, chunk in enumerate(chunks)
        ]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            print(f"Generated: {result.output_file}")


if __name__ == "__main__":
    main()
