"""Model registration and version tracking interfaces."""

from __future__ import annotations

from prediction.registry.model_version import ModelVersion
from prediction.registry.model_registry import ModelRegistry

__all__ = ["ModelVersion", "ModelRegistry"]
