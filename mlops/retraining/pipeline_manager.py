"""MLOps retraining pipeline coordinator."""

from __future__ import annotations

from typing import Any
from mlops.retraining.retraining_pipeline import RetrainingPipeline
from mlops.retraining.scheduler import RetrainingScheduler

class PipelineManager:
    """Manages trigger and schedule orchestration of model training runs."""

    def __init__(self) -> None:
        self.pipeline = RetrainingPipeline()
        self.scheduler = RetrainingScheduler()

    def run_training(self, model_name: str, dataset: str) -> dict[str, Any]:
        """Synchronously trigger model training pipeline simulation."""
        return self.pipeline.trigger_retraining(model_name, dataset)

    def schedule_run(self, model_name: str, interval: int) -> dict[str, Any]:
        """Register a schedule trigger definition for automated retraining."""
        return self.scheduler.schedule(model_name, interval)
