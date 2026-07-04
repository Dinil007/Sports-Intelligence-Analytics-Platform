"""Test MLOps drift detection."""

from __future__ import annotations

import unittest
from mlops.drift.data_drift import DataDriftDetector
from mlops.drift.model_drift import ModelDriftDetector
from mlops.drift.concept_drift import ConceptDriftDetector

class TestDrift(unittest.TestCase):
    """Test suite for drift detection algorithms."""

    def test_data_drift(self):
        baseline = [1.0, 1.1, 1.2, 1.3, 1.4]
        target = [1.0, 1.1, 1.2, 1.3, 1.4]
        res = DataDriftDetector.detect_drift(baseline, target)
        self.assertFalse(res["has_drift"])

    def test_model_drift(self):
        res = ModelDriftDetector.detect_drift(0.85, 0.78, threshold=0.05)
        self.assertTrue(res["has_drift"])
        self.assertAlmostEqual(res["accuracy_drop"], 0.07)

    def test_concept_drift(self):
        base_preds = [0.1, 0.2, 0.1, 0.2, 0.1]
        curr_preds = [0.5, 0.6, 0.5, 0.6, 0.5]
        res = ConceptDriftDetector.detect_drift(base_preds, curr_preds)
        self.assertTrue(res["has_drift"])
