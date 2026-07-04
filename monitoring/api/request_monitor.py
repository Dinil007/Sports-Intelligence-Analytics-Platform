"""API request tracker and statistics."""
from __future__ import annotations

import random
from typing import Dict, Any, List

def get_request_volume() -> int:
    """Returns simulated request volume in past 24 hours."""
    random.seed(42)
    return int(random.normalvariate(12500, 1500))

def get_request_trends() -> List[Dict[str, Any]]:
    """Get request trends over time (hourly) for Plotly line chart."""
    # Deterministic list of request counts for last 12 hours
    counts = [420, 480, 520, 610, 800, 950, 1100, 1050, 920, 780, 650, 500]
    trends = []
    for i, count in enumerate(counts):
        trends.append({
            "hour": f"-{12-i}h",
            "requests": count
        })
    return trends
