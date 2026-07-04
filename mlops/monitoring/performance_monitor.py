"""MLOps model functional performance monitoring."""

from __future__ import annotations

from typing import Any
from mlops.monitoring.prediction_monitor import PredictionMonitor
from mlops.monitoring.latency_monitor import LatencyMonitor
from mlops.monitoring.model_health import ModelHealthCalculator

class PerformanceMonitor:
    """Combines metrics, latency and model health to form central model observability."""

    def __init__(self) -> None:
        self.pred_monitor = PredictionMonitor()
        self.latency_monitor = LatencyMonitor()
        self.health_calculator = ModelHealthCalculator()

    def get_latest_observability(self, model_id: str, has_drift: bool) -> dict[str, Any]:
        """Aggregate all metrics into a single status report."""
        metrics = self.pred_monitor.get_metrics()
        model_metrics = [m for m in metrics if m["model_id"] == model_id]
        
        if not model_metrics:
            return {
                "model_id": model_id,
                "prediction_count": 0,
                "latency_ms": 0.0,
                "success_rate": 1.0,
                "failures": 0,
                "avg_confidence": 1.0,
                "latency_status": "Excellent",
                "health_index": 100.0
            }
            
        latest = model_metrics[-1]
        lat_status = self.latency_monitor.get_latency_status(latest["latency_ms"])
        health_idx = self.health_calculator.calculate_health_index(
            latest["success_rate"],
            latest["latency_ms"],
            has_drift
        )
        
        return {
            "model_id": model_id,
            "prediction_count": latest["prediction_count"],
            "latency_ms": latest["latency_ms"],
            "success_rate": latest["success_rate"],
            "failures": latest["failures"],
            "avg_confidence": latest["avg_confidence"],
            "latency_status": lat_status,
            "health_index": health_idx
        }
