"""Test MLOps experiments module."""

from __future__ import annotations

import unittest
from unittest.mock import patch, MagicMock
from mlops.experiments.experiment_metadata import ExperimentMetadata
from mlops.experiments.experiment_tracker import ExperimentTracker
from mlops.experiments.experiment_manager import ExperimentManager

class TestExperiments(unittest.TestCase):
    """Test suite for experiment manager and tracker."""

    @patch("mlops.experiments.experiment_storage.ExperimentStorage.save_all")
    @patch("mlops.experiments.experiment_storage.ExperimentStorage.load_all")
    def test_tracking_and_retrieval(self, mock_load, mock_save):
        mock_load.return_value = []
        mock_save.return_value = True

        tracker = ExperimentTracker()
        exp = tracker.track(
            experiment_id="exp_test",
            model_name="test_model",
            algorithm="test_algo",
            accuracy=0.85,
            precision=0.83,
            recall=0.84,
            f1=0.835,
            training_time=12.5,
            dataset="test_dataset",
            feature_count=10,
            model_version="1.0.0"
        )
        
        self.assertEqual(exp.experiment_id, "exp_test")
        self.assertEqual(exp.model_name, "test_model")
        self.assertEqual(exp.accuracy, 0.85)

    @patch("mlops.experiments.experiment_storage.ExperimentStorage.load_all")
    def test_comparison(self, mock_load):
        exp1 = ExperimentMetadata("1", "m", "a", 0.8, 0.8, 0.8, 0.8, 1.0, "d", 5, "1", "ts")
        exp2 = ExperimentMetadata("2", "m", "a", 0.9, 0.9, 0.9, 0.9, 2.0, "d", 5, "1", "ts")
        mock_load.return_value = [exp1, exp2]

        mgr = ExperimentManager()
        compared = mgr.compare(["1"])
        self.assertEqual(len(compared), 1)
        self.assertEqual(compared[0].experiment_id, "1")
