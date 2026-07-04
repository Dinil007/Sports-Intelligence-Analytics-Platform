"""MLOps model operational health metrics."""

from __future__ import annotations

class ModelHealthCalculator:
    """Calculates operational health indexes based on latency, failure rates, and drift."""

    @staticmethod
    def calculate_health_index(
        success_rate: float,
        avg_latency_ms: float,
        has_drift: bool
    ) -> float:
        """Calculate aggregate health index score (0-100)."""
        # Starting score
        score = 100.0
        
        # Penalize for failure rate
        failure_penalty = (1.0 - success_rate) * 200.0
        score -= min(failure_penalty, 40.0)
        
        # Penalize for latency > 200ms
        if avg_latency_ms > 200.0:
            score -= 15.0
        elif avg_latency_ms > 100.0:
            score -= 5.0
            
        # Penalize for drift
        if has_drift:
            score -= 25.0
            
        return max(0.0, score)
