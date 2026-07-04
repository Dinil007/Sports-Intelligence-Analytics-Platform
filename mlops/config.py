"""MLOps configuration."""

from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MLOPS_DIR = PROJECT_ROOT / "data" / "mlops"

# Ensure data directory exists
MLOPS_DIR.mkdir(parents=True, exist_ok=True)

class MLOpsConfig:
    """Config settings for MLOps platform."""
    STORAGE_DIR: Path = MLOPS_DIR
    EXPERIMENT_STORAGE_PATH: Path = MLOPS_DIR / "experiments.json"
    MODEL_REGISTRY_PATH: Path = MLOPS_DIR / "model_registry.json"
    FEATURE_STORE_PATH: Path = MLOPS_DIR / "feature_store.json"
    RETRAINING_HISTORY_PATH: Path = MLOPS_DIR / "retraining_history.json"
    DEPLOYMENT_HISTORY_PATH: Path = MLOPS_DIR / "deployment_history.json"
    MONITORING_METRICS_PATH: Path = MLOPS_DIR / "monitoring_metrics.json"
