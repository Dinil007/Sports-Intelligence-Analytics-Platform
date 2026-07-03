"""Kafka message deserialization utility."""

from __future__ import annotations

import json
from typing import Any, Dict

class EventDeserializer:
    """Deserializes binary stream payloads into Python dictionaries."""
    
    @staticmethod
    def deserialize(data: bytes) -> Dict[str, Any]:
        """Convert binary payload back to dict."""
        if not data:
            return {}
        try:
            return json.loads(data.decode("utf-8"))
        except Exception:
            return {}
