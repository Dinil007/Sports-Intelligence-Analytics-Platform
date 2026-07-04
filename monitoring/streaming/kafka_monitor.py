"""Kafka broker connection and throughput stats."""
from __future__ import annotations

import random
from typing import Dict, Any, List

def get_broker_status() -> Dict[str, Any]:
    """Return status of Kafka broker connection."""
    return {
        "status": "Connected",
        "brokers_count": 3,
        "active_controllers": 1,
        "throughput_mb_sec": 4.82,
    }

def get_throughput_history() -> List[Dict[str, Any]]:
    """Return historical Kafka throughput for Line charts."""
    rates = [2.1, 3.4, 4.2, 4.8, 5.1, 4.9, 4.2, 3.8, 4.5, 4.7, 5.0, 4.82]
    history = []
    for i, val in enumerate(rates):
        history.append({
            "hour": f"-{12-i}h",
            "throughput_mb_sec": val
        })
    return history
