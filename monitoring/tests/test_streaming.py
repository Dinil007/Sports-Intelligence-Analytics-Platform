"""Unit tests for streaming monitoring."""
from __future__ import annotations

import unittest
from monitoring.streaming.stream_monitor import check_streaming_health
from monitoring.streaming.kafka_monitor import get_broker_status, get_throughput_history
from monitoring.streaming.consumer_monitor import get_consumers_status
from monitoring.streaming.producer_monitor import get_producers_status

class TestStreamingMonitoring(unittest.TestCase):
    """Test cases for Kafka stream pipeline monitoring."""
    
    def test_streaming_health(self) -> None:
        health = check_streaming_health()
        self.assertEqual(health["status"], "Healthy")
        
    def test_broker(self) -> None:
        broker = get_broker_status()
        self.assertEqual(broker["status"], "Connected")
        self.assertEqual(len(get_throughput_history()), 12)
        
    def test_consumers_and_producers(self) -> None:
        self.assertTrue(len(get_consumers_status()) > 0)
        self.assertTrue(len(get_producers_status()) > 0)
