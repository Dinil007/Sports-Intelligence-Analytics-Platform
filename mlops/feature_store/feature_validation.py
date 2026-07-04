"""MLOps feature validation logic."""

from __future__ import annotations

from typing import Any

class FeatureValidation:
    """Validates features for correct data types, format, and ranges."""

    @staticmethod
    def validate(value: Any, value_type: str) -> bool:
        """Validate if a value conforms to its registered value type."""
        try:
            if value_type.lower() == "float":
                float(value)
                return True
            elif value_type.lower() == "int":
                int(value)
                return True
            elif value_type.lower() == "bool":
                return isinstance(value, bool) or str(value).lower() in ("true", "false", "0", "1")
            elif value_type.lower() == "str":
                return isinstance(value, str)
            return False
        except (ValueError, TypeError):
            return False
        return False
