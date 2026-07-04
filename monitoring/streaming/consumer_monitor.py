"""Kafka consumers lag and group monitoring."""
from __future__ import annotations

import random
from typing import List, Dict, Any

def get_consumers_status() -> List[Dict[str, Any]]:
    """Return consumer groups and their lag metric."""
    return [
        {"group": "prediction-processor", "topic": "sports-events", "lag": 0, "status": "Active"},
        {"group": "metrics-archiver", "topic": "predictions", "lag": 12, "status": "Active"},
        {"group": "alert-trigger", "topic": "predictions", "lag": 2, "status": "Active"},
    ]

def get_consumer_lag_trends() -> List[Dict[str, Any]]:
    """Consumer lag history over time for Plotly Line chart."""
    lags = [0, 4, 18, 25, 12, 5, 2, 8, 14, 22, 10, 5]
    history = []
    for i, val in enumerate(lags):
        history.append({
            "hour": f"-{12-i}h",
            "consumer_lag": val
        })
    return history
