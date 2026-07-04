"""MLOps experiment tracker module."""

from __future__ import annotations

from typing import Any
from mlops.experiments.experiment_metadata import ExperimentMetadata
from mlops.experiments.experiment_storage import ExperimentStorage
from mlops.utils.time_utils import get_current_iso_timestamp

class ExperimentTracker:
    """Manages tracking single experiments and saving them."""

    def __init__(self) -> None:
        self.storage = ExperimentStorage()

    def track(
        self,
        experiment_id: str,
        model_name: str,
        algorithm: str,
        accuracy: float,
        precision: float,
        recall: float,
        f1: float,
        training_time: float,
        dataset: str,
        feature_count: int,
        model_version: str
    ) -> ExperimentMetadata:
        """Track a new run/experiment and save it."""
        metadata = ExperimentMetadata(
            experiment_id=experiment_id,
            model_name=model_name,
            algorithm=algorithm,
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1=f1,
            training_time=training_time,
            dataset=dataset,
            feature_count=feature_count,
            model_version=model_version,
            timestamp=get_current_iso_timestamp()
        )
        
        experiments = self.storage.load_all()
        # Remove if duplicate experiment ID exists
        experiments = [e for e in experiments if e.experiment_id != experiment_id]
        experiments.append(metadata)
        self.storage.save_all(experiments)
        return metadata
