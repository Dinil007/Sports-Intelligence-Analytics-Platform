"""MLOps stage transition manager."""

from __future__ import annotations

from mlops.registry.model_lifecycle import ModelLifecycle

class StageManager:
    """Transitions models between staging environment target configurations."""

    def __init__(self) -> None:
        self.lifecycle = ModelLifecycle()

    def transition_stage(self, model_id: str, version: str, stage: str) -> bool:
        """Execute model stage promotion definition."""
        return self.lifecycle.promote(model_id, stage)
