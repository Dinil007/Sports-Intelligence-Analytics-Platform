"""MLOps model lifecycle management."""

from __future__ import annotations

from typing import Any
from mlops.constants import VALID_STAGES, STAGE_DEVELOPMENT
from mlops.registry.production_registry import ProductionRegistry
from mlops.utils.time_utils import get_current_iso_timestamp

class ModelLifecycle:
    """Manages model transitions between lifecycle stages."""

    def __init__(self) -> None:
        self.registry = ProductionRegistry()

    def register(self, model_id: str, name: str, version: str, description: str = "") -> dict[str, Any]:
        """Register a new model in the registry."""
        data = self.registry.load_registry()
        model_entry = {
            "model_id": model_id,
            "name": name,
            "version": version,
            "stage": STAGE_DEVELOPMENT,
            "description": description,
            "registered_at": get_current_iso_timestamp(),
            "updated_at": get_current_iso_timestamp()
        }
        data[model_id] = model_entry
        self.registry.save_registry(data)
        return model_entry

    def promote(self, model_id: str, target_stage: str) -> bool:
        """Promote a registered model to a new lifecycle stage."""
        if target_stage not in VALID_STAGES:
            return False
            
        data = self.registry.load_registry()
        if model_id not in data:
            return False
            
        data[model_id]["stage"] = target_stage
        data[model_id]["updated_at"] = get_current_iso_timestamp()
        return self.registry.save_registry(data)

    def list_models(self) -> list[dict[str, Any]]:
        """List all registered models."""
        data = self.registry.load_registry()
        return list(data.values())
