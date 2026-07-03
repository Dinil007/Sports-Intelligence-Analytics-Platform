"""Kafka and Simulated Event Consumer."""

from __future__ import annotations

import time
from typing import Any, Dict, Generator, List, Optional
from streaming.config import config
from streaming.constants import (
    TOPIC_MATCH_EVENTS,
    TOPIC_PLAYER_EVENTS,
    TOPIC_TEAM_EVENTS,
    TOPIC_SYSTEM_EVENTS,
)
from streaming.kafka.connection import connection_manager
from streaming.kafka.event_deserializer import EventDeserializer
from streaming.logging import logger

_CONSUMERS: Dict[str, Any] = {}

def create_consumer(topic: str) -> Any:
    """Initialize and cache the Kafka or Simulated Consumer client for a given topic."""
    global _CONSUMERS
    if topic in _CONSUMERS:
        return _CONSUMERS[topic]
        
    logger.info(f"Initializing Streaming Event Consumer for topic '{topic}'...")
    if connection_manager.simulate:
        logger.info(f"Consumer for topic '{topic}' running in simulated mode.")
        _CONSUMERS[topic] = f"simulated-consumer-active-{topic}"
    else:
        try:
            from kafka import KafkaConsumer # type: ignore
            _CONSUMERS[topic] = KafkaConsumer(
                topic,
                bootstrap_servers=config.BOOTSTRAP_SERVERS,
                group_id=config.GROUP_ID,
                client_id=f"{config.CLIENT_ID}-{topic}",
                enable_auto_commit=True,
                auto_offset_reset="earliest",
            )
            logger.info(f"KafkaConsumer for topic '{topic}' initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize real KafkaConsumer for '{topic}': {e}. Falling back to simulation.")
            connection_manager.simulate = True
            _CONSUMERS[topic] = f"simulated-consumer-active-{topic}"
            
    return _CONSUMERS[topic]

def consume_match_events(max_count: int = 10, timeout_seconds: float = 1.0) -> Generator[Dict[str, Any], None, None]:
    """Consume match event records from match-events topic."""
    yield from _consume_topic_events(TOPIC_MATCH_EVENTS, max_count, timeout_seconds)

def consume_player_events(max_count: int = 10, timeout_seconds: float = 1.0) -> Generator[Dict[str, Any], None, None]:
    """Consume player event records from player-events topic."""
    yield from _consume_topic_events(TOPIC_PLAYER_EVENTS, max_count, timeout_seconds)

def consume_team_events(max_count: int = 10, timeout_seconds: float = 1.0) -> Generator[Dict[str, Any], None, None]:
    """Consume team event records from team-events topic."""
    yield from _consume_topic_events(TOPIC_TEAM_EVENTS, max_count, timeout_seconds)

def consume_system_events(max_count: int = 10, timeout_seconds: float = 1.0) -> Generator[Dict[str, Any], None, None]:
    """Consume system event records from system-events topic."""
    yield from _consume_topic_events(TOPIC_SYSTEM_EVENTS, max_count, timeout_seconds)

def close_consumer(topic: str) -> None:
    """Clean up and close the consumer for a topic."""
    global _CONSUMERS
    if topic not in _CONSUMERS:
        return
    logger.info(f"Closing consumer for topic '{topic}'...")
    consumer = _CONSUMERS.pop(topic)
    if not connection_manager.simulate and hasattr(consumer, "close"):
        try:
            consumer.close()
        except Exception as e:
            logger.error(f"Error closing KafkaConsumer for '{topic}': {e}")

def _consume_topic_events(topic: str, max_count: int, timeout_seconds: float) -> Generator[Dict[str, Any], None, None]:
    """Helper method to run consumption from Kafka or Simulation."""
    consumer = create_consumer(topic)
    count = 0
    start_time = time.time()
    
    if connection_manager.simulate:
        while count < max_count and (time.time() - start_time) < timeout_seconds:
            payload = connection_manager.consume_simulated(topic, timeout=0.1)
            if payload is not None:
                event = EventDeserializer.deserialize(payload)
                if event:
                    yield event
                    count += 1
            else:
                time.sleep(0.05)
    else:
        # Real Kafka consumption using poll
        if hasattr(consumer, "poll"):
            timeout_ms = int(timeout_seconds * 1000)
            records = consumer.poll(timeout_ms=timeout_ms, max_records=max_count - count)
            for _, partition_records in records.items():
                for record in partition_records:
                    if count >= max_count:
                        break
                    event = EventDeserializer.deserialize(record.value)
                    if event:
                        yield event
                        count += 1
                    if count >= max_count:
                        break
