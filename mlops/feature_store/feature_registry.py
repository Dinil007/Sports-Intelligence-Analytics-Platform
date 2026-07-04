"""MLOps feature registration."""

from __future__ import annotations

from typing import Any
from mlops.feature_store.feature_store import FeatureStore
from mlops.utils.time_utils import get_current_iso_timestamp

class FeatureRegistry:
    """Manages registering new features in the feature store."""

    def __init__(self) -> None:
        self.store = FeatureStore()

    def register_feature(self, name: str, entity: str, value_type: str, description: str = "") -> dict[str, Any]:
        """Register a new feature into the feature store."""
        data = self.store.load_store()
        feature_entry = {
            "name": name,
            "entity": entity,
            "value_type": value_type,
            "description": description,
            "created_at": get_current_iso_timestamp()
        }
        data[name] = feature_entry
        self.store.save_store(data)
        return feature_entry
