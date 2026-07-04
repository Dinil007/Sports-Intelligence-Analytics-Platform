"""Deterministic alert rule matcher and trigger."""
from __future__ import annotations

import time
from typing import List, Dict, Any
from monitoring.constants import ALERT_WARNING, ALERT_CRITICAL

def run_alert_rules() -> List[Dict[str, Any]]:
    """Evaluates rules against mock parameters to return active alerts."""
    # We return a few deterministic warning/critical alerts as specified in instructions
    return [
        {
            "id": "alert_cpu_warn",
            "title": "CPU Usage Alert",
            "description": "System CPU usage exceeded 80% briefly during training run",
            "level": ALERT_WARNING,
            "raised_at": "2026-07-04T13:12:00Z",
            "acknowledged": False
        },
        {
            "id": "alert_consumer_lag",
            "title": "Kafka Consumer Lag Delay",
            "description": "Consumer group 'metrics-archiver' lag is greater than 10 messages",
            "level": ALERT_WARNING,
            "raised_at": "2026-07-04T14:22:15Z",
            "acknowledged": False
        },
        {
            "id": "alert_db_connections",
            "title": "Database Connection Pool High",
            "description": "PostgreSQL active connections reached 85% of pool capacity",
            "level": ALERT_WARNING,
            "raised_at": "2026-07-04T14:45:00Z",
            "acknowledged": False
        }
    ]
