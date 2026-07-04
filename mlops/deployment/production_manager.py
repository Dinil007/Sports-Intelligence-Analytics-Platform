"""MLOps production environment promoter."""

from __future__ import annotations

from mlops.constants import STAGE_PRODUCTION
from mlops.registry.model_lifecycle import ModelLifecycle

class ProductionManager:
    """Promotes verified models to final production server status."""

    def __init__(self) -> None:
        self.lifecycle = ModelLifecycle()

    def promote_to_production(self, model_id: str, version: str) -> bool:
        """Promote the model to Production stage."""
        return self.lifecycle.promote(model_id, STAGE_PRODUCTION)
