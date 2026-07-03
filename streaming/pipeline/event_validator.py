"""Validation module for live streaming events."""

from __future__ import annotations

from typing import Any, Dict, Tuple, Optional
from datetime import datetime
from streaming.constants import VALID_EVENT_TYPES
from streaming.logging import logger

class EventValidator:
    """Validates structural and domain properties of incoming football events."""
    
    @staticmethod
    def validate_event(event: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate an event dictionary.
        
        Returns:
            (is_valid, error_reason)
        """
        # 1. Event ID Validation
        if not event.get("event_id"):
            return False, "Missing 'event_id'"
            
        # 2. Timestamp Validation
        timestamp = event.get("timestamp")
        if not timestamp:
            return False, "Missing 'timestamp'"
        if isinstance(timestamp, str):
            try:
                datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            except ValueError:
                return False, f"Invalid ISO timestamp format: {timestamp}"
        elif not isinstance(timestamp, (datetime, int, float)):
            return False, f"Invalid timestamp type: {type(timestamp)}"
            
        # 3. Event Type Validation
        event_type = event.get("event_type")
        if not event_type:
            return False, "Missing 'event_type'"
        if str(event_type).upper() not in VALID_EVENT_TYPES:
            return False, f"Unsupported event type: '{event_type}'"
            
        # 4. Player and Team ID Validation (if present, must be integers)
        player_id = event.get("player_id")
        if player_id is not None:
            try:
                int(player_id)
            except (ValueError, TypeError):
                return False, f"Invalid player_id: '{player_id}' (must be integer)"
                
        team_id = event.get("team_id")
        if team_id is not None:
            try:
                int(team_id)
            except (ValueError, TypeError):
                return False, f"Invalid team_id: '{team_id}' (must be integer)"

        # 5. Coordinates Validation (if present, must be pair of floats between 0 and 100)
        coords = event.get("coordinates")
        if coords is not None:
            if not isinstance(coords, (list, tuple)) or len(coords) != 2:
                return False, "Coordinates must be a list/tuple of length 2"
            try:
                x, y = float(coords[0]), float(coords[1])
                if not (0.0 <= x <= 100.0) or not (0.0 <= y <= 100.0):
                    return False, f"Coordinates out of bounds (0-100 scale): ({x}, {y})"
            except (ValueError, TypeError):
                return False, f"Coordinates must be numeric values: {coords}"

        return True, None
