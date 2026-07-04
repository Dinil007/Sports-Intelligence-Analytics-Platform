"""MLOps storage abstractions."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from mlops.utils.serialization import load_json, save_json

class MLOpsStorage:
    """Handles thread-safe reading and writing of JSON database files."""

    def __init__(self, file_path: Path) -> None:
        self.file_path: Path = file_path

    def read(self) -> Any:
        return load_json(self.file_path, default=[])

    def write(self, data: Any) -> bool:
        return save_json(self.file_path, data)
