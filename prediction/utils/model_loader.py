"""Version-aware model loader using registry lookups."""

from __future__ import annotations

from typing import Any, Optional
from prediction.registry.model_registry import ModelRegistry
from prediction.utils.serialization import ModelSerializer
from prediction.logging import logger

class ModelLoader:
    """Enterprise class for retrieving model instances by name and version."""
    
    @staticmethod
    def load_model(model_name: str, version: Optional[str] = None) -> Any:
        """Query the registry and load the specified model binary from disk."""
        meta = ModelRegistry.get_model_metadata(model_name, version=version)
        if not meta:
            raise ValueError(f"No registered metadata found for model '{model_name}' (version: {version or 'latest'}).")
            
        location = meta["location"]
        # Location is usually filename relative to config.MODELS_DIR or absolute path string
        import os
        filename = os.path.basename(location)
        logger.info(f"Loading registered model '{model_name}' ({meta['version']}) from '{filename}'...")
        return ModelSerializer.load(filename)
