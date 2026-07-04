"""MLOps concept drift detection."""

from __future__ import annotations

import numpy as np

class ConceptDriftDetector:
    """Detects if statistical properties of target variable change over time."""

    @staticmethod
    def detect_drift(baseline_predictions: list[float], current_predictions: list[float]) -> dict[str, float | bool]:
        """Detect drift by checking significant mean changes in target predictions."""
        if not baseline_predictions or not current_predictions:
            return {"mean_diff": 0.0, "has_drift": False}
        
        base_mean = np.mean(baseline_predictions)
        curr_mean = np.mean(current_predictions)
        
        diff = abs(base_mean - curr_mean)
        # Simple heuristic threshold: if mean changes by more than 15% of baseline mean
        threshold = 0.15 * max(abs(base_mean), 1e-5)
        has_drift = diff >= threshold
        
        return {
            "mean_diff": float(diff),
            "has_drift": bool(has_drift)
        }
