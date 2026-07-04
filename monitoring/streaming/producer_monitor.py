"""Kafka producers error rate and throughput stats."""
from __future__ import annotations

from typing import List, Dict, Any

def get_producers_status() -> List[Dict[str, Any]]:
    """Return status of all registered publishers/producers."""
    return [
        {"producer_id": "event-streamer-01", "success_rate_percent": 99.98, "status": "Active"},
        {"producer_id": "analytics-dispatcher-02", "success_rate_percent": 100.0, "status": "Active"},
    ]
