"""MLOps experiment storage handler."""

from __future__ import annotations

from typing import Any
from mlops.config import MLOpsConfig
from mlops.experiments.experiment_metadata import ExperimentMetadata
from mlops.utils.storage import MLOpsStorage

class ExperimentStorage:
    """Handles persistence of experiments to disk."""

    def __init__(self) -> None:
        self.storage = MLOpsStorage(MLOpsConfig.EXPERIMENT_STORAGE_PATH)

    def load_all(self) -> list[ExperimentMetadata]:
        """Load all tracked experiments."""
        raw_list = self.storage.read()
        if not isinstance(raw_list, list):
            return []
        return [ExperimentMetadata.from_dict(item) for item in raw_list]

    def save_all(self, experiments: list[ExperimentMetadata]) -> bool:
        """Save all experiments back to storage."""
        raw_list = [exp.to_dict() for exp in experiments]
        return self.storage.write(raw_list)
