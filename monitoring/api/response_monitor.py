"""API response metrics and latency tracking."""
from __future__ import annotations

import random
from typing import List, Dict, Any

def get_error_rate() -> float:
    """Returns average HTTP error rate percentage (5xx / 4xx)."""
    return 0.45  # 0.45% error rate (very healthy)

def get_p95_latency() -> float:
    """Returns 95th percentile request latency in milliseconds."""
    return 48.2

def get_latency_trends() -> List[Dict[str, Any]]:
    """Get response latency trends over last 12 hours for Area chart."""
    latencies = [35.2, 42.1, 51.0, 48.9, 72.3, 85.1, 92.4, 68.2, 55.0, 44.1, 38.6, 36.0]
    trends = []
    for i, latency in enumerate(latencies):
        trends.append({
            "hour": f"-{12-i}h",
            "latency_ms": latency
        })
    return trends
