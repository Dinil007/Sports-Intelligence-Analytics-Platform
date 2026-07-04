"""MLOps centralized drift detector."""

from __future__ import annotations

from typing import Any
from mlops.drift.data_drift import DataDriftDetector
from mlops.drift.model_drift import ModelDriftDetector
from mlops.drift.concept_drift import ConceptDriftDetector

class DriftDetector:
    """Consolidated drift detection engine."""

    def __init__(self) -> None:
        self.data_detector = DataDriftDetector()
        self.model_detector = ModelDriftDetector()
        self.concept_detector = ConceptDriftDetector()

    def run_all_checks(
        self,
        baseline_features: list[float],
        target_features: list[float],
        baseline_acc: float,
        current_acc: float,
        baseline_preds: list[float],
        current_preds: list[float]
    ) -> dict[str, Any]:
        """Perform all data, model and concept drift checks."""
        data_res = self.data_detector.detect_drift(baseline_features, target_features)
        model_res = self.model_detector.detect_drift(baseline_acc, current_acc)
        concept_res = self.concept_detector.detect_drift(baseline_preds, current_preds)
        
        return {
            "data_drift": data_res,
            "model_drift": model_res,
            "concept_drift": concept_res,
            "overall_drift_detected": (
                data_res["has_drift"] or
                model_res["has_drift"] or
                concept_res["has_drift"]
            )
        }
