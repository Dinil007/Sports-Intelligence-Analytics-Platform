"""Test MLOps retraining pipelines."""

from __future__ import annotations

import unittest
from unittest.mock import patch, MagicMock
from mlops.retraining.pipeline_manager import PipelineManager
from mlops.retraining.scheduler import RetrainingScheduler

class TestRetraining(unittest.TestCase):
    """Test suite for retraining orchestration."""

    @patch("mlops.retraining.retraining_pipeline.RetrainingPipeline.trigger_retraining")
    def test_run_retraining(self, mock_trigger):
        mock_trigger.return_value = {"status": "Success"}
        mgr = PipelineManager()
        res = mgr.run_training("goals_predictor", "dataset")
        self.assertEqual(res["status"], "Success")

    def test_scheduler(self):
        sched = RetrainingScheduler()
        res = sched.schedule("goals_predictor", 7)
        self.assertEqual(res["status"], "Scheduled")
        self.assertEqual(res["interval_days"], 7)
