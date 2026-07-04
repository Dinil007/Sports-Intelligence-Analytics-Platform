"""Observability for model health and availability status."""
from __future__ import annotations

from typing import List, Dict, Any
from monitoring.constants import STATUS_HEALTHY

def check_models_status() -> List[Dict[str, Any]]:
    """Return status details of active and serving ML models."""
    return [
        {
            "model_id": "goals_predictor",
            "version": "1.0.0",
            "status": STATUS_HEALTHY,
            "accuracy_metric": 0.84,
            "last_serving_at": "2026-07-04T14:48:10Z"
        },
        {
            "model_id": "injury_classifier",
            "version": "0.9.5",
            "status": STATUS_HEALTHY,
            "accuracy_metric": 0.89,
            "last_serving_at": "2026-07-04T14:51:32Z"
        }
    ]
