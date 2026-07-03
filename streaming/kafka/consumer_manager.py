"""Lifecycle manager for event consumers."""

from __future__ import annotations

from typing import Any, Callable, Dict
from streaming.kafka.consumer import create_consumer, close_consumer
from streaming.logging import logger

class ConsumerManager:
    """Enterprise manager for handling streaming consumer lifecycle and event loops."""
    
    def __init__(self) -> None:
        self._active_consumers: Dict[str, Any] = {}
        
    def register_consumer(self, topic: str) -> None:
        """Create and register a consumer for a specific topic."""
        consumer = create_consumer(topic)
        self._active_consumers[topic] = consumer
        logger.info(f"Registered consumer for topic '{topic}' in ConsumerManager.")
        
    def deregister_consumer(self, topic: str) -> None:
        """Close and remove a consumer registration."""
        close_consumer(topic)
        self._active_consumers.pop(topic, None)
        logger.info(f"Deregistered consumer for topic '{topic}' in ConsumerManager.")

    def run_worker_loop(self, topic: str, handler: Callable[[Dict[str, Any]], None], max_events: int = 100) -> int:
        """Run a single-pass worker poll loop for a topic, executing handler on messages."""
        from streaming.kafka.consumer import _consume_topic_events
        logger.info(f"Worker loop polling topic '{topic}'...")
        processed_count = 0
        for event in _consume_topic_events(topic, max_count=max_events, timeout_seconds=2.0):
            try:
                handler(event)
                processed_count += 1
            except Exception as e:
                logger.error(f"Error handling event in worker loop: {e}")
        logger.info(f"Worker loop complete for topic '{topic}'. Processed {processed_count} messages.")
        return processed_count

    def stop_all(self) -> None:
        """Shut down all registered consumers cleanly."""
        topics = list(self._active_consumers.keys())
        for topic in topics:
            self.deregister_consumer(topic)
        logger.info("All consumers stopped in ConsumerManager.")
