"""Kafka and Simulated Event Producer."""

from __future__ import annotations

from typing import Any, Dict, Optional, Union
from pydantic import BaseModel

from streaming.config import config
from streaming.constants import (
    TOPIC_MATCH_EVENTS,
    TOPIC_PLAYER_EVENTS,
    TOPIC_TEAM_EVENTS,
    TOPIC_SYSTEM_EVENTS,
)
from streaming.kafka.connection import connection_manager
from streaming.kafka.event_serializer import EventSerializer
from streaming.logging import logger

_PRODUCER: Optional[Any] = None

def create_producer() -> Any:
    """Initialize and cache the Kafka or Simulated Producer client."""
    global _PRODUCER
    if _PRODUCER is not None:
        return _PRODUCER
        
    logger.info("Initializing Streaming Event Producer...")
    if connection_manager.simulate:
        logger.info("Producer running in simulated mode.")
        _PRODUCER = "simulated-producer-active"
    else:
        try:
            from kafka import KafkaProducer # type: ignore
            _PRODUCER = KafkaProducer(
                bootstrap_servers=config.BOOTSTRAP_SERVERS,
                client_id=config.CLIENT_ID,
                acks=config.ACKS,
                retries=config.RETRIES,
                retry_backoff_ms=config.RETRY_BACKOFF_MS,
                batch_size=config.BATCH_SIZE,
                linger_ms=config.LINGER_MS,
            )
            logger.info("KafkaProducer initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize real KafkaProducer: {e}. Falling back to simulation.")
            connection_manager.simulate = True
            _PRODUCER = "simulated-producer-active"
            
    return _PRODUCER

def publish_match_event(event: Union[BaseModel, Dict[str, Any]]) -> bool:
    """Publish a football match event to match-events topic."""
    return _send_to_topic(TOPIC_MATCH_EVENTS, event)

def publish_player_event(event: Union[BaseModel, Dict[str, Any]]) -> bool:
    """Publish an event to player-events topic."""
    return _send_to_topic(TOPIC_PLAYER_EVENTS, event)

def publish_team_event(event: Union[BaseModel, Dict[str, Any]]) -> bool:
    """Publish an event to team-events topic."""
    return _send_to_topic(TOPIC_TEAM_EVENTS, event)

def publish_system_event(event: Union[BaseModel, Dict[str, Any]]) -> bool:
    """Publish a system health or status event to system-events topic."""
    return _send_to_topic(TOPIC_SYSTEM_EVENTS, event)

def flush_events() -> None:
    """Force flush all buffered producer messages."""
    global _PRODUCER
    if _PRODUCER is None:
        return
    logger.info("Flushing event producer buffer...")
    if not connection_manager.simulate and hasattr(_PRODUCER, "flush"):
        _PRODUCER.flush()

def close_producer() -> None:
    """Clean up and close the event producer."""
    global _PRODUCER
    if _PRODUCER is None:
        return
    logger.info("Closing event producer...")
    flush_events()
    if not connection_manager.simulate and hasattr(_PRODUCER, "close"):
        _PRODUCER.close()
    _PRODUCER = None

def _send_to_topic(topic: str, event: Union[BaseModel, Dict[str, Any]]) -> bool:
    """Helper function to serialize and send events to a topic."""
    producer = create_producer()
    try:
        payload = EventSerializer.serialize(event)
        if connection_manager.simulate:
            connection_manager.publish_simulated(topic, payload)
        else:
            if hasattr(producer, "send"):
                producer.send(topic, value=payload)
        return True
    except Exception as e:
        logger.error(f"Failed to publish event to topic '{topic}': {e}")
        return False
