"""User active session tracking."""
from __future__ import annotations

from typing import List, Dict, Any

def get_session_statistics() -> Dict[str, Any]:
    """Return simulated session statistics."""
    return {
        "active_sessions": 4,
        "average_session_duration_minutes": 24.5,
    }

def get_session_trends() -> List[Dict[str, Any]]:
    """Return historical active session count for Area chart."""
    sessions = [1, 1, 1, 2, 3, 4, 4, 3, 2, 2, 1, 1]
    history = []
    for i, val in enumerate(sessions):
        history.append({
            "hour": f"-{12-i}h",
            "active_sessions": val
        })
    return history
