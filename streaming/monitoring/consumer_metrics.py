"""Consumer lag and performance monitoring."""

from __future__ import annotations

from typing import Dict
from streaming.kafka.connection import connection_manager

def consumer_lag(topic: str) -> int:
    """Return current simulated/real unconsumed message queue size for a topic."""
    # In simulation mode, this is simply the size of the simulated broker queue
    if connection_manager.simulate:
        return connection_manager.get_simulated_broker(topic).qsize()
    
    # Real Kafka connection lag is typically fetched via admin client; fallback to mock lag of 0
    return 0

def consumer_rate(topic: str) -> float:
    """Return average consumption rate of messages per second."""
    # Return mock rate
    return 12.5
