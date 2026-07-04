"""Database slow query logger and tracker."""
from __future__ import annotations

from typing import List, Dict, Any

def get_slow_queries() -> List[Dict[str, Any]]:
    """Simulated query performance logs."""
    return [
        {
            "query": "SELECT * FROM player_metrics JOIN player_scouting ON ...",
            "duration_ms": 320.5,
            "called_at": "2026-07-04T12:01:45Z"
        },
        {
            "query": "SELECT SUM(xg) FROM match_events GROUP BY player_id...",
            "duration_ms": 180.2,
            "called_at": "2026-07-04T13:42:10Z"
        }
    ]
