"""MLOps deployment status registry."""

from __future__ import annotations

from typing import Any
from mlops.config import MLOpsConfig
from mlops.utils.storage import MLOpsStorage
from mlops.utils.time_utils import get_current_iso_timestamp

class DeploymentRegistry:
    """Tracks deployed models and deployment events/history."""

    def __init__(self) -> None:
        self.storage = MLOpsStorage(MLOpsConfig.DEPLOYMENT_HISTORY_PATH)

    def log_deployment(self, model_id: str, version: str, stage: str, status: str) -> dict[str, Any]:
        """Log a new deployment event."""
        history = self.storage.read()
        if not isinstance(history, list):
            history = []
            
        event = {
            "model_id": model_id,
            "version": version,
            "stage": stage,
            "status": status,
            "timestamp": get_current_iso_timestamp()
        }
        history.append(event)
        self.storage.write(history)
        return event

    def get_history(self) -> list[dict[str, Any]]:
        """Retrieve deployment history."""
        history = self.storage.read()
        if isinstance(history, list):
            return history
        return []
