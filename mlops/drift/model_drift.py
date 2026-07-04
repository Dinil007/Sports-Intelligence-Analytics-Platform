"""MLOps model performance drift detection."""

from __future__ import annotations

class ModelDriftDetector:
    """Calculates accuracy degradation of deployed model over time."""

    @staticmethod
    def detect_drift(baseline_accuracy: float, current_accuracy: float, threshold: float = 0.05) -> dict[str, float | bool]:
        """Detect drift based on drop in model accuracy compared to baseline."""
        drop = baseline_accuracy - current_accuracy
        has_drift = drop >= threshold
        return {
            "accuracy_drop": float(drop),
            "has_drift": bool(has_drift)
        }
