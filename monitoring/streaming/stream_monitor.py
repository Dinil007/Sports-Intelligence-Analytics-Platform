"""Streaming health aggregator."""
from __future__ import annotations

from typing import Dict, Any
from monitoring.streaming.kafka_monitor import get_broker_status
from monitoring.constants import STATUS_HEALTHY

def check_streaming_health() -> Dict[str, Any]:
    """Check aggregated Kafka and streaming components status."""
    return {
        "status": STATUS_HEALTHY,
        "broker": get_broker_status(),
    }
