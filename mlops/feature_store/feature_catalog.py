"""MLOps feature catalog search and query."""

from __future__ import annotations

from typing import Any
from mlops.feature_store.feature_store import FeatureStore

class FeatureCatalog:
    """Queries and lists registered features in the catalog."""

    def __init__(self) -> None:
        self.store = FeatureStore()

    def list_features(self) -> list[dict[str, Any]]:
        """List all features currently registered."""
        data = self.store.load_store()
        return list(data.values())

    def get_feature(self, name: str) -> dict[str, Any] | None:
        """Get a single feature definition by name."""
        data = self.store.load_store()
        return data.get(name)
