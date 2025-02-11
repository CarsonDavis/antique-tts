# Text-to-Speech CLI

A modular command-line interface for text-to-speech synthesis, supporting multiple TTS engines. The CLI handles text chunking, parallel processing, and provides a unified interface across different TTS services.

## Features

- Supports multiple TTS engines (currently OpenAI and Kokoro)
- Automatic text chunking with configurable chunk sizes
- Parallel processing with multiple workers
- Cost estimation and confirmation for paid services
- Modular design for easy addition of new TTS engines

## Quick Start

### Installation

```bash
git clone https://github.com/CarsonDavis/antique-tts.git
cd antique-tts
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Environment Setup

For OpenAI TTS, you'll need to set your API key:

```bash
# Linux/MacOS
export OPENAI_API_KEY='your-api-key-here'

# Windows (PowerShell)
$env:OPENAI_API_KEY='your-api-key-here'

# Windows (Command Prompt)
set OPENAI_API_KEY=your-api-key-here
```

Get your API key from: https://platform.openai.com/account/api-keys

### Basic Usage

Convert text to speech using default settings (Kokoro engine):

```bash
python cli.py input.txt --output-dir ./output_audio
```

### Using Kokoro Engine with Custom Voice

```bash
python cli.py input.txt --output-dir ./output_audio --engine kokoro --voice am_michael --speed 1.2
```

### Using OpenAI Engine

```bash
python cli.py input.txt --output-dir ./output_audio --engine openai --voice alloy

Estimated cost: $0.53
Do you want to proceed? (y/N): y
```

## Configuration Options

### Common Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--output-dir` | Output directory for audio files | `output` |
| `--chunk-size` | Maximum characters per chunk | 4000 |
| `--max-workers` | Number of parallel workers | 4 |

### Kokoro Engine Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--lang-code` | Language code for synthesis | "a" |
| `--speed` | Speech speed multiplier | 1.0 |
| `--voice` | Voice to use `af_bella`, `af_nicole`, `af_sarah`, `af_sky`, `bf_emma`, `bf_isabella`, `am_adam`, `am_michael`, `bm_george`, `bm_lewis`| "am_michael" |


### OpenAI Engine Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--model` | OpenAI TTS model | "tts-1-hd" |
| `--voice` | Voice to use: `alloy`, `ash`, `coral`, `echo`, `fable`, `onyx`, `nova`, `sage`, `shimmer`| "alloy" |
| `--response-format` | Audio format for output | "wav" |

Available OpenAI voices: `alloy`, `ash`, `coral`, `echo`, `fable`, `onyx`, `nova`, `sage`, `shimmer`

## Full Usage

```bash
usage: cli.py [-h] [--engine {kokoro,openai}] [--output-dir OUTPUT_DIR] 
              [--chunk-size CHUNK_SIZE] [--max-workers MAX_WORKERS] 
              [--lang-code LANG_CODE] [--speed SPEED] [--voice VOICE] 
              [--model MODEL] [--response-format RESPONSE_FORMAT] 
              input_file
```

See all available settings:
```bash
python cli.py --help
```

## Adding New Engines

The project is designed to be easily extensible. To add a new TTS engine:

1. Create a new engine configuration class in `tts_engine/config.py`
2. Create a new engine implementation class in `tts_engine/`
3. Register the engine/config mapping in `tts_engine/registry.py`

## Dependencies

- NLTK for text chunking
- SoundFile for audio processing
- Pydantic for configuration management
- OpenAI and Kokoro SDKs for respective engines
