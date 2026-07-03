"""Utilities for managing and parsing model versions."""

from __future__ import annotations

import re

class ModelVersion:
    """Helper class to validate, increment, and format model semantic versions."""
    
    @staticmethod
    def is_valid(version: str) -> bool:
        """Return True if the version follows 'vX' format where X is integer >= 1."""
        return bool(re.match(r"^v\d+$", version))

    @staticmethod
    def increment(version: str) -> str:
        """Increment a version string, e.g., 'v1' -> 'v2'."""
        if not ModelVersion.is_valid(version):
            return "v1"
        num = int(version[1:])
        return f"v{num + 1}"

    @staticmethod
    def initial() -> str:
        """Return the initial version string."""
        return "v1"
