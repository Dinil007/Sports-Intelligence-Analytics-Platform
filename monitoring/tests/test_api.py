"""Unit tests for API monitoring."""
from __future__ import annotations

import unittest
from monitoring.api.api_monitor import check_api_health
from monitoring.api.request_monitor import get_request_volume, get_request_trends
from monitoring.api.response_monitor import get_error_rate, get_p95_latency
from monitoring.api.endpoint_statistics import get_top_endpoints

class TestApiMonitoring(unittest.TestCase):
    """Test cases for API usage monitoring."""
    
    def test_api_health(self) -> None:
        health = check_api_health()
        self.assertIn("status", health)
        self.assertIn("error_rate_percent", health)
        
    def test_requests(self) -> None:
        vol = get_request_volume()
        self.assertTrue(vol > 0)
        trends = get_request_trends()
        self.assertEqual(len(trends), 12)
        
    def test_responses(self) -> None:
        self.assertTrue(get_error_rate() >= 0)
        self.assertTrue(get_p95_latency() > 0)
        
    def test_endpoints(self) -> None:
        endpoints = get_top_endpoints()
        self.assertTrue(len(endpoints) > 0)
        self.assertIn("endpoint", endpoints[0])
