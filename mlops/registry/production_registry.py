"""MLOps model registry storage and query."""

from __future__ import annotations

from typing import Any
from mlops.config import MLOpsConfig
from mlops.utils.storage import MLOpsStorage

class ProductionRegistry:
    """Manages reading and writing registered models in production."""

    def __init__(self) -> None:
        self.storage = MLOpsStorage(MLOpsConfig.MODEL_REGISTRY_PATH)

    def load_registry(self) -> dict[str, Any]:
        """Load registered models. Returns dictionary of model keys to attributes."""
        res = self.storage.read()
        if isinstance(res, dict):
            return res
        return {}

    def save_registry(self, registry_data: dict[str, Any]) -> bool:
        """Save registry data back to disk."""
        return self.storage.write(registry_data)
