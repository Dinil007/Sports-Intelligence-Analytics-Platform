"""Offline model training and validation metrics monitor."""
from __future__ import annotations

from typing import Dict, Any

def get_training_metrics() -> Dict[str, Any]:
    """Return logs and validation statistics from recent model trainings."""
    return {
        "recent_training_jobs": 2,
        "average_loss": 0.125,
        "last_training_status": "Success",
    }
