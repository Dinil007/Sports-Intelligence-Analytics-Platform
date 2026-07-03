"""Joblib-based serialization helper functions for model artifacts."""

from __future__ import annotations

import joblib # type: ignore
from pathlib import Path
from typing import Any
from prediction.config import config
from prediction.logging import logger

class ModelSerializer:
    """Handles version-aware saving and loading of model artifacts to the disk."""

    @staticmethod
    def save(model: Any, filename: str) -> Path:
        """Serialize a model or preprocessing object to joblib format on disk."""
        dest_path = config.MODELS_DIR / filename
        try:
            joblib.dump(model, dest_path)
            logger.info(f"Serialized and saved model to '{dest_path}' successfully.")
            return dest_path
        except Exception as e:
            logger.error(f"Failed to serialize model to '{dest_path}': {e}")
            raise e

    @staticmethod
    def load(filename: str) -> Any:
        """Load a serialized model object from joblib format on disk."""
        src_path = config.MODELS_DIR / filename
        if not src_path.exists():
            raise FileNotFoundError(f"No serialized model found at '{src_path}'.")
        try:
            model = joblib.load(src_path)
            logger.info(f"Loaded and deserialized model from '{src_path}' successfully.")
            return model
        except Exception as e:
            logger.error(f"Failed to deserialize model from '{src_path}': {e}")
            raise e
