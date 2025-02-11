# utils/file_manager.py
from pathlib import Path
import os
import soundfile as sf


class FileManager:
    @staticmethod
    def create_output_dir(path: Path) -> Path:
        path.mkdir(parents=True, exist_ok=True)
        return path.resolve()  # Return absolute path

    @staticmethod
    def safe_write_audio(path: Path, audio_data, sample_rate=24000):
        """Atomic audio write with soundfile"""
        temp_path = path.with_name(f".tmp_{path.name}")
        sf.write(temp_path, audio_data, sample_rate)
        os.replace(temp_path, path)
