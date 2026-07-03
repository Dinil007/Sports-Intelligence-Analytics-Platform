"""Thread-safe connection broker manager for Kafka & in-memory simulation."""

from __future__ import annotations

import queue
from typing import Any, Dict, List, Optional
from collections import defaultdict
from streaming.config import config
from streaming.logging import logger

# Thread-safe in-memory message brokers for simulation mode
_SIMULATED_BROKERS: Dict[str, queue.Queue[bytes]] = defaultdict(queue.Queue)

class KafkaConnection:
    """Manages active producers/consumers connection handles with simulated fallbacks."""
    
    def __init__(self) -> None:
        self.simulate: bool = config.SIMULATE_BROKER
        self._producer_instance: Any = None
        self._consumer_instances: Dict[str, Any] = {}
        
        # Test imports of kafka-python
        try:
            import kafka # type: ignore
            logger.info("kafka-python package is available.")
        except ImportError:
            logger.warning("kafka-python package not found. Running in simulation mode.")
            self.simulate = True

    def get_simulated_broker(self, topic: str) -> queue.Queue[bytes]:
        """Get the queue representing a Kafka topic for testing."""
        return _SIMULATED_BROKERS[topic]

    def publish_simulated(self, topic: str, value: bytes) -> None:
        """Publish bytes into the in-memory queue."""
        self.get_simulated_broker(topic).put(value)
        logger.debug(f"[Simulation] Published {len(value)} bytes to '{topic}'")

    def consume_simulated(self, topic: str, timeout: float = 0.5) -> Optional[bytes]:
        """Fetch bytes from the in-memory queue."""
        q = self.get_simulated_broker(topic)
        try:
            return q.get(timeout=timeout)
        except queue.Empty:
            return None

connection_manager = KafkaConnection()
