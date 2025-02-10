# Antique-TTS

Batch process text files into audiobooks using modern TTS engines.

## Installation
```bash
git clone https://github.com/CarsonDavis/antique-tts.git
cd antique-tts
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Basic Usage
```bash
python cli.py INPUT_FILE [--output-dir DIR] [--engine ENGINE] [--chunk-size SIZE]
```

**Required Arguments**:
- `INPUT_FILE`: Path to text file to convert

**Key Options**:
- `--output-dir`: Output directory (default: ./output)
- `--engine`: `kokoro` (default) or `openai`
- `--chunk-size`: Max characters per audio chunk (default: 4000)
- `--workers`: Parallel processing threads (default: 4)
- `--voice`: Voice model (default: am_michael)

## Example: Create Audiobook
```bash
python cli.py books/buffon.txt \
  --output-dir ./buffon_audio \
  --chunk-size 5000 \
  --workers 8 \
  --voice am_michael
```

## Output Structure
```
buffon_audio/
├── segment_0000_0.wav
├── segment_0001_0.wav
└── metadata.json
```

## Configuration Options
See all available settings:
```bash
python cli.py --help
```
