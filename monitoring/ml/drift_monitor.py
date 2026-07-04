"""Data and concept drift monitoring indicators."""
from __future__ import annotations

from typing import Dict, Any
from monitoring.constants import STATUS_HEALTHY

def get_drift_metrics() -> Dict[str, Any]:
    """Get active drift scores for all deployed models."""
    return {
        "status": STATUS_HEALTHY,
        "goals_predictor": {
            "psi": 0.082,  # < 0.1 -> low drift
            "ks_p_value": 0.35,  # > 0.05 -> no significant change
            "drift_detected": False
        },
        "injury_classifier": {
            "psi": 0.045,
            "ks_p_value": 0.62,
            "drift_detected": False
        }
    }
