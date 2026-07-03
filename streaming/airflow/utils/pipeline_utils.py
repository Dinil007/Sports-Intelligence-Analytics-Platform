"""Airflow DAG processing utilities."""

from __future__ import annotations

from typing import Any, Dict, List
from streaming.logging import logger

def extract_live_batch(match_id: int) -> List[Dict[str, Any]]:
    """Simulate extracting raw live match events."""
    logger.info(f"Extracting live match events for match_id: {match_id}")
    return [
        {
            "event_id": f"event-{match_id}-1",
            "timestamp": "2026-07-03T12:00:00Z",
            "event_type": "PASS",
            "player_id": 1,
            "team_id": 1,
            "coordinates": [50.0, 50.0],
            "match_id": match_id,
        },
        {
            "event_id": f"event-{match_id}-2",
            "timestamp": "2026-07-03T12:01:00Z",
            "event_type": "SHOT",
            "player_id": 2,
            "team_id": 1,
            "coordinates": [85.5, 48.2],
            "match_id": match_id,
        }
    ]
