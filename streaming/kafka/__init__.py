"""Kafka connection, topic registry, serialization, producer, and consumer interfaces."""

from __future__ import annotations

from streaming.kafka.topics import register_topics
from streaming.kafka.event_serializer import EventSerializer
from streaming.kafka.event_deserializer import EventDeserializer
from streaming.kafka.connection import connection_manager
from streaming.kafka.producer import (
    create_producer,
    publish_match_event,
    publish_player_event,
    publish_team_event,
    publish_system_event,
    flush_events,
    close_producer,
)
from streaming.kafka.consumer import (
    create_consumer,
    consume_match_events,
    consume_player_events,
    consume_team_events,
    consume_system_events,
    close_consumer,
)
from streaming.kafka.producer_manager import ProducerManager
from streaming.kafka.consumer_manager import ConsumerManager

__all__ = [
    "register_topics",
    "EventSerializer",
    "EventDeserializer",
    "connection_manager",
    "create_producer",
    "publish_match_event",
    "publish_player_event",
    "publish_team_event",
    "publish_system_event",
    "flush_events",
    "close_producer",
    "create_consumer",
    "consume_match_events",
    "consume_player_events",
    "consume_team_events",
    "consume_system_events",
    "close_consumer",
    "ProducerManager",
    "ConsumerManager",
]
