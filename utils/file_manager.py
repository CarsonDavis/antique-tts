# utils/file_manager.py
from pathlib import Path
import datetime
import os


class FileManager:
    @staticmethod
    def create_output_dir(path: Path) -> Path:
        path.mkdir(parents=True, exist_ok=True)
        return path.resolve()  # Return absolute path

    @staticmethod
    def safe_write(path: Path, data: bytes) -> None:
        temp_path = path.with_name(f".tmp_{path.name}")
        with open(temp_path, "wb") as f:
            f.write(data)
        os.replace(temp_path, path)
