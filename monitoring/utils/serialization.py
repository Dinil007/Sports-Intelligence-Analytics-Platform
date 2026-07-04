"""Serialization utilities for monitoring data."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

def load_json(file_path: Path, default: Any = None) -> Any:
    """Safely load JSON data from path."""
    if not file_path.exists():
        return default if default is not None else {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default if default is not None else {}

def save_json(file_path: Path, data: Any) -> bool:
    """Safely save JSON data to path."""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, default=str)
        return True
    except Exception:
        return False
