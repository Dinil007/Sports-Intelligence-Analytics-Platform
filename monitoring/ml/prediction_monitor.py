"""Aggregated prediction engine statistics."""
from __future__ import annotations

import random
from typing import Dict, Any, List

def get_prediction_stats() -> Dict[str, Any]:
    """Get active predictions throughput and statistics."""
    return {
        "active_serving_models": 2,
        "total_predictions_24h": 41250,
        "average_inference_time_ms": 14.8,
        "p95_inference_time_ms": 28.5,
    }

def get_prediction_throughput_trends() -> List[Dict[str, Any]]:
    """Prediction throughput history over last 12 hours for Line chart."""
    rates = [2200, 2450, 2900, 3100, 3800, 4200, 4800, 4300, 3900, 3400, 2800, 2500]
    history = []
    for i, val in enumerate(rates):
        history.append({
            "hour": f"-{12-i}h",
            "predictions_count": val
        })
    return history
