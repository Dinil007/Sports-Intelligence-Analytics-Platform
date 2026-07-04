"""MLOps retraining training history registry."""

from __future__ import annotations

from typing import Any
from mlops.config import MLOpsConfig
from mlops.utils.storage import MLOpsStorage

class TrainingHistory:
    """Manages accessing the database of previous training executions."""

    def __init__(self) -> None:
        self.storage = MLOpsStorage(MLOpsConfig.RETRAINING_HISTORY_PATH)

    def get_history(self) -> list[dict[str, Any]]:
        """Retrieve previous retraining run logs."""
        res = self.storage.read()
        if isinstance(res, list):
            return res
        return []
