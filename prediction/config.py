"""Configuration settings for models training and inference."""

from __future__ import annotations

import os
from pathlib import Path

class PredictionConfig:
    """Class holding prediction module configuration parameter values."""
    
    PREDICTION_ROOT: Path = Path(__file__).resolve().parent
    MODELS_DIR: Path = PREDICTION_ROOT / "serialized_models"
    REGISTRY_PATH: Path = PREDICTION_ROOT / "registry.json"

    # Default model params
    RANDOM_STATE: int = 42
    DEFAULT_TEST_SIZE: float = 0.2
    
    # Preprocessing
    IMPUTE_STRATEGY: str = "mean"
    SCALING_STRATEGY: str = "standard"

    def __init__(self) -> None:
        self.MODELS_DIR.mkdir(parents=True, exist_ok=True)

config = PredictionConfig()
