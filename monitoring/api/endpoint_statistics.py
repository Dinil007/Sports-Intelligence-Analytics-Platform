"""API endpoint usage statistics."""
from __future__ import annotations

from typing import List, Dict, Any

def get_top_endpoints() -> List[Dict[str, Any]]:
    """Return top endpoints sorted by call count."""
    return [
        {"endpoint": "/api/v1/predictions/live", "calls": 4820, "avg_latency_ms": 12.4},
        {"endpoint": "/api/v1/players/compare", "calls": 3150, "avg_latency_ms": 95.8},
        {"endpoint": "/api/v1/scouting/reports", "calls": 2100, "avg_latency_ms": 45.2},
        {"endpoint": "/api/v1/chat/ask", "calls": 1850, "avg_latency_ms": 220.1},
        {"endpoint": "/api/v1/transfer/adviser", "calls": 920, "avg_latency_ms": 180.4},
    ]
