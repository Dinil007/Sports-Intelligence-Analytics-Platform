"""Unit tests for the Streaming Event Producer."""

from __future__ import annotations

import unittest
from datetime import datetime, timezone
from streaming.kafka.producer import (
    create_producer,
    publish_match_event,
    publish_player_event,
    publish_team_event,
    publish_system_event,
    close_producer,
)
from streaming.kafka.connection import connection_manager
from streaming.constants import (
    TOPIC_MATCH_EVENTS,
    TOPIC_PLAYER_EVENTS,
    TOPIC_TEAM_EVENTS,
    TOPIC_SYSTEM_EVENTS,
)

class TestProducer(unittest.TestCase):
    """Verify event publishing across topics in mock/simulation mode."""
    
    def setUp(self) -> None:
        # Enforce simulation mode for testing
        connection_manager.simulate = True
        create_producer()
        # Drain mock queue before each test
        for topic in [TOPIC_MATCH_EVENTS, TOPIC_PLAYER_EVENTS, TOPIC_TEAM_EVENTS, TOPIC_SYSTEM_EVENTS]:
            q = connection_manager.get_simulated_broker(topic)
            while not q.empty():
                q.get_nowait()

    def test_publish_match_event(self) -> None:
        event = {
            "event_id": "evt-101",
            "timestamp": datetime.now(timezone.utc),
            "event_type": "PASS",
            "match_id": 101,
            "player_id": 1,
            "team_id": 1,
            "coordinates": [45.5, 60.2],
        }
        success = publish_match_event(event)
        self.assertTrue(success)
        self.assertEqual(connection_manager.get_simulated_broker(TOPIC_MATCH_EVENTS).qsize(), 1)

    def test_publish_player_event(self) -> None:
        event = {
            "event_id": "evt-102",
            "timestamp": datetime.now(timezone.utc),
            "event_type": "SHOT",
            "player_id": 2,
        }
        success = publish_player_event(event)
        self.assertTrue(success)
        self.assertEqual(connection_manager.get_simulated_broker(TOPIC_PLAYER_EVENTS).qsize(), 1)

    def test_publish_team_event(self) -> None:
        event = {
            "event_id": "evt-103",
            "timestamp": datetime.now(timezone.utc),
            "event_type": "GOAL",
            "team_id": 1,
        }
        success = publish_team_event(event)
        self.assertTrue(success)
        self.assertEqual(connection_manager.get_simulated_broker(TOPIC_TEAM_EVENTS).qsize(), 1)

    def tearDown(self) -> None:
        close_producer()

if __name__ == "__main__":
    unittest.main()
