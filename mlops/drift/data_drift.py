"""MLOps data drift detection."""

from __future__ import annotations

import numpy as np
from mlops.utils.metrics import calculate_psi

class DataDriftDetector:
    """Calculates population stability and feature value shift between baseline and target."""

    @staticmethod
    def detect_drift(baseline: list[float], target: list[float]) -> dict[str, float | bool]:
        """Detect drift by calculating PSI between baseline and target distributions."""
        psi = calculate_psi(baseline, target)
        # Standard threshold: PSI > 0.2 represents significant drift, PSI > 0.1 is moderate
        has_drift = psi >= 0.1
        return {
            "psi": psi,
            "has_drift": has_drift
        }
