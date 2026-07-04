"""MLOps prediction requests monitoring."""

from __future__ import annotations

from typing import Any
from mlops.config import MLOpsConfig
from mlops.utils.storage import MLOpsStorage
from mlops.utils.time_utils import get_current_iso_timestamp

class PredictionMonitor:
    """Logs and reads real-time inference prediction stats (latency, throughput, confidence)."""

    def __init__(self) -> None:
        self.storage = MLOpsStorage(MLOpsConfig.MONITORING_METRICS_PATH)

    def log_predictions(
        self,
        model_id: str,
        count: int,
        latency_ms: float,
        success_rate: float,
        failures: int,
        avg_confidence: float
    ) -> dict[str, Any]:
        """Save a new set of prediction health metrics to storage."""
        history = self.storage.read()
        if not isinstance(history, list):
            history = []
            
        entry = {
            "model_id": model_id,
            "prediction_count": count,
            "latency_ms": latency_ms,
            "success_rate": success_rate,
            "failures": failures,
            "avg_confidence": avg_confidence,
            "timestamp": get_current_iso_timestamp()
        }
        history.append(entry)
        self.storage.write(history)
        return entry

    def get_metrics(self) -> list[dict[str, Any]]:
        """List historical monitor entries."""
        res = self.storage.read()
        if isinstance(res, list):
            return res
        return []
