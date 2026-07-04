"""MLOps experiment manager module."""

from __future__ import annotations

from typing import Any
from mlops.experiments.experiment_metadata import ExperimentMetadata
from mlops.experiments.experiment_storage import ExperimentStorage

class ExperimentManager:
    """Handles query, retrieval, and comparison operations on tracked experiments."""

    def __init__(self) -> None:
        self.storage = ExperimentStorage()

    def list_all(self) -> list[ExperimentMetadata]:
        """List all tracked experiments."""
        return self.storage.load_all()

    def compare(self, experiment_ids: list[str]) -> list[ExperimentMetadata]:
        """Filter and return specific experiments for side-by-side comparison."""
        all_exps = self.storage.load_all()
        id_set = set(experiment_ids)
        return [e for e in all_exps if e.experiment_id in id_set]
