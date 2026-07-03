"""Transformation and normalization module for streaming events."""

from __future__ import annotations

from typing import Any, Dict
from streaming.utils.time_utils import parse_timestamp, format_iso_timestamp
from streaming.logging import logger

class EventTransformer:
    """Normalizes event schema, coordinates, timestamps, and key metric names."""
    
    @staticmethod
    def transform(event: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize event details into a standard canonical schema."""
        transformed = dict(event)
        
        # 1. Normalize Timestamp to UTC ISO format string
        raw_ts = transformed.get("timestamp")
        if raw_ts:
            dt = parse_timestamp(raw_ts)
            transformed["timestamp"] = format_iso_timestamp(dt)
            
        # 2. Normalize Coordinates (ensure coordinates is a tuple, rounding values)
        coords = transformed.get("coordinates")
        if coords is not None:
            try:
                x = round(float(coords[0]), 2)
                y = round(float(coords[1]), 2)
                transformed["coordinates"] = (x, y)
            except (ValueError, TypeError):
                pass
                
        # 3. Standardize Metric Names / Keys
        # Map fields from various sources (e.g. opta, statsbomb formats)
        metric_mappings = {
            "player": "player_id",
            "team": "team_id",
            "type": "event_type",
            "action": "event_type",
            "id": "event_id",
            "x_coord": "coordinates",
            "y_coord": "coordinates",
        }
        
        for legacy_key, canonical_key in metric_mappings.items():
            if legacy_key in transformed and canonical_key not in transformed:
                val = transformed.pop(legacy_key)
                if canonical_key == "coordinates" and "y_coord" in event and "x_coord" in event:
                    try:
                        transformed["coordinates"] = (float(event["x_coord"]), float(event["y_coord"]))
                    except (ValueError, TypeError):
                        pass
                else:
                    transformed[canonical_key] = val
                    
        # 4. Standardize Event Type to upper case
        if "event_type" in transformed:
            transformed["event_type"] = str(transformed["event_type"]).upper().strip()

        return transformed
