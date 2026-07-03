"""JSON-backed Model Registry for tracking trained models metadata."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from prediction.config import config
from prediction.registry.model_version import ModelVersion
from prediction.logging import logger

class ModelRegistry:
    """Enterprise registry for logging and querying model artifacts and metadata."""

    @staticmethod
    def _load_registry() -> Dict[str, List[Dict[str, Any]]]:
        if not config.REGISTRY_PATH.exists():
            return {}
        try:
            with open(config.REGISTRY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to read model registry: {e}")
            return {}

    @staticmethod
    def _save_registry(registry_data: Dict[str, List[Dict[str, Any]]]) -> None:
        try:
            with open(config.REGISTRY_PATH, "w", encoding="utf-8") as f:
                json.dump(registry_data, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to write model registry: {e}")

    @staticmethod
    def register_model(
        model_name: str,
        algorithm: str,
        metrics: Dict[str, float],
        location: str,
        status: str = "candidate",
    ) -> str:
        """Register a new model version, saving its metadata to the central registry.
        
        Returns the version string allocated.
        """
        registry = ModelRegistry._load_registry()
        
        if model_name not in registry:
            registry[model_name] = []
            
        # Determine next version
        history = registry[model_name]
        if not history:
            version = ModelVersion.initial()
        else:
            latest = history[-1]["version"]
            version = ModelVersion.increment(latest)
            
        entry = {
            "model_name": model_name,
            "algorithm": algorithm,
            "version": version,
            "training_date": datetime.now(timezone.utc).isoformat(),
            "metrics": metrics,
            "status": status,
            "location": location,
        }
        
        registry[model_name].append(entry)
        ModelRegistry._save_registry(registry)
        logger.info(f"Registered model '{model_name}' version '{version}' successfully.")
        return version

    @staticmethod
    def get_model_metadata(model_name: str, version: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Retrieve metadata for a specific model name and version (or latest if version is None)."""
        registry = ModelRegistry._load_registry()
        history = registry.get(model_name)
        if not history:
            return None
            
        if version is None:
            # Return latest production or latest general entry
            prod_models = [m for m in history if m["status"] == "production"]
            return prod_models[-1] if prod_models else history[-1]
            
        for entry in history:
            if entry["version"] == version:
                return entry
        return None

    @staticmethod
    def update_status(model_name: str, version: str, status: str) -> bool:
        """Update registration status (e.g. 'production', 'archived')."""
        registry = ModelRegistry._load_registry()
        history = registry.get(model_name)
        if not history:
            return False
            
        updated = False
        for entry in history:
            if entry["version"] == version:
                entry["status"] = status
                updated = True
                break
                
        if updated:
            ModelRegistry._save_registry(registry)
            logger.info(f"Updated status of '{model_name}' version '{version}' to '{status}'.")
        return updated
