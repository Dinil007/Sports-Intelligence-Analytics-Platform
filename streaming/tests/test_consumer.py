"""Unit tests for the Streaming Event Consumer."""

from __future__ import annotations

import unittest
from datetime import datetime, timezone
from streaming.kafka.producer import publish_match_event, create_producer
from streaming.kafka.consumer import consume_match_events, close_consumer
from streaming.kafka.connection import connection_manager
from streaming.constants import TOPIC_MATCH_EVENTS

class TestConsumer(unittest.TestCase):
    """Verify event consumption routines in simulated broker mode."""
    
    def setUp(self) -> None:
        connection_manager.simulate = True
        create_producer()
        # Drain mock queue before each test
        q = connection_manager.get_simulated_broker(TOPIC_MATCH_EVENTS)
        while not q.empty():
            q.get_nowait()

    def test_consume_match_events(self) -> None:
        # Publish an event
        event = {
            "event_id": "evt-c1",
            "timestamp": datetime.now(timezone.utc),
            "event_type": "PASS",
            "match_id": 101,
        }
        publish_match_event(event)
        
        # Consume the event
        consumed = list(consume_match_events(max_count=1, timeout_seconds=0.5))
        self.assertEqual(len(consumed), 1)
        self.assertEqual(consumed[0]["event_id"], "evt-c1")
        self.assertEqual(consumed[0]["event_type"], "PASS")

    def tearDown(self) -> None:
        close_consumer(TOPIC_MATCH_EVENTS)

if __name__ == "__main__":
    unittest.main()
