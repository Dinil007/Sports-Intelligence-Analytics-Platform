"""Unit tests for ML models monitoring."""
from __future__ import annotations

import unittest
from monitoring.ml.prediction_monitor import get_prediction_stats, get_prediction_throughput_trends
from monitoring.ml.model_monitor import check_models_status
from monitoring.ml.drift_monitor import get_drift_metrics
from monitoring.ml.training_monitor import get_training_metrics

class TestMlMonitoring(unittest.TestCase):
    """Test cases for ML model serving and drift tracking."""
    
    def test_prediction_stats(self) -> None:
        stats = get_prediction_stats()
        self.assertTrue(stats["active_serving_models"] > 0)
        self.assertEqual(len(get_prediction_throughput_trends()), 12)
        
    def test_models_status(self) -> None:
        models = check_models_status()
        self.assertTrue(len(models) > 0)
        self.assertIn("accuracy_metric", models[0])
        
    def test_drift_and_training(self) -> None:
        drift = get_drift_metrics()
        self.assertIn("status", drift)
        self.assertIn("goals_predictor", drift)
        
        train = get_training_metrics()
        self.assertEqual(train["last_training_status"], "Success")
