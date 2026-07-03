"""Kafka message serialization utility."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict, Union
from pydantic import BaseModel

class EventSerializer:
    """Serializes event structures into bytes for transmission."""
    
    @staticmethod
    def serialize(event: Union[BaseModel, Dict[str, Any]]) -> bytes:
        """Convert a Pydantic model or dictionary into JSON UTF-8 bytes."""
        if isinstance(event, BaseModel):
            event_dict = event.model_dump()
        else:
            event_dict = dict(event)
            
        return json.dumps(event_dict, default=EventSerializer._datetime_handler).encode("utf-8")

    @staticmethod
    def _datetime_handler(obj: Any) -> str:
        if isinstance(obj, datetime):
            return obj.isoformat().replace("+00:00", "Z")
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
