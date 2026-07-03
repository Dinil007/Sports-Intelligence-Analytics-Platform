"""Lifecycle manager for event producers."""

from __future__ import annotations

from typing import Any, Dict, Union
from pydantic import BaseModel
from streaming.kafka.producer import create_producer, close_producer, flush_events
from streaming.logging import logger

class ProducerManager:
    """Enterprise manager for handling streaming producer lifecycle and bulk sends."""
    
    def __init__(self) -> None:
        self._producer: Any = None
        
    def start(self) -> None:
        """Initialize the producer resources."""
        self._producer = create_producer()
        logger.info("Producer Manager started and producer initialized.")
        
    def stop(self) -> None:
        """Close producer resources and flush remaining buffers."""
        close_producer()
        self._producer = None
        logger.info("Producer Manager stopped.")
        
    def send_batch(self, topic: str, events: list[Union[BaseModel, Dict[str, Any]]]) -> int:
        """Send a batch of events to the specified topic and flush."""
        from streaming.kafka.producer import _send_to_topic
        success_count = 0
        for event in events:
            if _send_to_topic(topic, event):
                success_count += 1
        flush_events()
        logger.info(f"Batched {success_count}/{len(events)} events sent to topic '{topic}'.")
        return success_count
