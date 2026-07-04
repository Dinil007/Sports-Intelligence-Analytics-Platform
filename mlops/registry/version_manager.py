"""MLOps model version management."""

from __future__ import annotations

import re
from typing import Any

class VersionManager:
    """Helper class to validate and parse semantic versions of models."""

    @staticmethod
    def is_valid_version(version: str) -> bool:
        """Validate if model version follows semantic versioning (e.g., 1.2.3)."""
        pattern = r"^\d+\.\d+\.\d+$"
        return bool(re.match(pattern, version))

    @staticmethod
    def increment_patch(version: str) -> str:
        """Increment patch version (e.g. 1.2.3 -> 1.2.4)."""
        if not VersionManager.is_valid_version(version):
            return version
        major, minor, patch = map(int, version.split("."))
        return f"{major}.{minor}.{patch + 1}"
