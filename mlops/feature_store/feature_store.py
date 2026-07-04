"""MLOps feature store interface."""

from __future__ import annotations

from typing import Any
from mlops.config import MLOpsConfig
from mlops.utils.storage import MLOpsStorage

class FeatureStore:
    """Provides high-level database access for reusable ML features."""

    def __init__(self) -> None:
        self.storage = MLOpsStorage(MLOpsConfig.FEATURE_STORE_PATH)

    def load_store(self) -> dict[str, Any]:
        """Load feature store database dictionary."""
        data = self.storage.read()
        if isinstance(data, dict):
            return data
        return {}

    def save_store(self, data: dict[str, Any]) -> bool:
        """Save feature store database dictionary."""
        return self.storage.write(data)
