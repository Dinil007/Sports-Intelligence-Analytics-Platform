"""MLOps deployment rollback controller."""

from __future__ import annotations

from mlops.constants import STAGE_ROLLBACK
from mlops.registry.model_lifecycle import ModelLifecycle

class RollbackManager:
    """Manages active rollback of model deployments to previous stable version configurations."""

    def __init__(self) -> None:
        self.lifecycle = ModelLifecycle()

    def execute_rollback(self, model_id: str, previous_version: str) -> bool:
        """Rollback registered model stage status to Rollback state."""
        return self.lifecycle.promote(model_id, STAGE_ROLLBACK)
