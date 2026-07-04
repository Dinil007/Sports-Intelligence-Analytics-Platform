"""Database connections tracker."""
from __future__ import annotations

import random
from typing import List, Dict, Any

def get_active_connections() -> int:
    """Returns count of active DB connection pool sessions."""
    return 14

def get_connection_history() -> List[Dict[str, Any]]:
    """Connection pool history over time for Plotly Line chart."""
    connections = [8, 12, 14, 15, 14, 13, 11, 10, 12, 14, 16, 14]
    history = []
    for i, count in enumerate(connections):
        history.append({
            "hour": f"-{12-i}h",
            "active_connections": count
        })
    return history
