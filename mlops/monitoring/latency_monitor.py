"""MLOps prediction latency monitor."""

from __future__ import annotations

class LatencyMonitor:
    """Calculates and aggregates system performance response times."""

    @staticmethod
    def get_latency_status(avg_latency_ms: float) -> str:
        """Categorize system latency health status."""
        if avg_latency_ms < 50.0:
            return "Excellent"
        elif avg_latency_ms < 150.0:
            return "Good"
        elif avg_latency_ms < 300.0:
            return "Warning"
        return "Critical"
