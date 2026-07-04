"""Test MLOps monitoring and health indicators."""

from __future__ import annotations

import unittest
from unittest.mock import patch, MagicMock
from mlops.monitoring.prediction_monitor import PredictionMonitor
from mlops.monitoring.latency_monitor import LatencyMonitor
from mlops.monitoring.model_health import ModelHealthCalculator

class TestMonitoring(unittest.TestCase):
    """Test suite for telemetry monitoring."""

    @patch("mlops.monitoring.prediction_monitor.PredictionMonitor.get_metrics")
    @patch("mlops.monitoring.prediction_monitor.PredictionMonitor.log_predictions")
    def test_log_predictions(self, mock_log, mock_get):
        mock_log.return_value = {"prediction_count": 100}
        monitor = PredictionMonitor()
        entry = monitor.log_predictions("test_id", 100, 25.0, 0.99, 1, 0.95)
        self.assertEqual(entry["prediction_count"], 100)

    def test_latency_status(self):
        self.assertEqual(LatencyMonitor.get_latency_status(30.0), "Excellent")
        self.assertEqual(LatencyMonitor.get_latency_status(120.0), "Good")
        self.assertEqual(LatencyMonitor.get_latency_status(250.0), "Warning")
        self.assertEqual(LatencyMonitor.get_latency_status(350.0), "Critical")

    def test_health_calculator(self):
        score_perfect = ModelHealthCalculator.calculate_health_index(1.0, 30.0, False)
        self.assertEqual(score_perfect, 100.0)
        
        score_drifted = ModelHealthCalculator.calculate_health_index(1.0, 30.0, True)
        self.assertEqual(score_drifted, 75.0)
        
        score_failing = ModelHealthCalculator.calculate_health_index(0.90, 30.0, False)
        self.assertEqual(score_failing, 80.0)
