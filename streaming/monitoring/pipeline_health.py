"""Monitoring metrics for streaming pipeline health."""

from __future__ import annotations

from typing import Any, Dict
from streaming.pipeline.pipeline_manager import PipelineManager
from streaming.logging import logger

# Global manager reference for monitoring
_ACTIVE_PIPELINES: Dict[str, PipelineManager] = {}

def register_monitored_pipeline(manager: PipelineManager) -> None:
    """Register a pipeline manager instance for monitoring."""
    _ACTIVE_PIPELINES[manager.pipeline_id] = manager

def get_pipeline_status(pipeline_id: str = "live-football-ingest") -> Dict[str, Any]:
    """Retrieve runtime status parameters of a registered pipeline."""
    manager = _ACTIVE_PIPELINES.get(pipeline_id)
    if not manager:
        return {"pipeline_id": pipeline_id, "status": "UNKNOWN", "is_active": False}
        
    status = manager.get_status()
    return status.model_dump()

def get_pipeline_health(pipeline_id: str = "live-football-ingest") -> str:
    """Calculate and return high-level health state (HEALTHY, DEGRADED, UNHEALTHY)."""
    manager = _ACTIVE_PIPELINES.get(pipeline_id)
    if not manager:
        return "UNKNOWN"
        
    status = manager.get_status()
    if not status.is_active:
        return "INACTIVE"
        
    # If error rate is high, flag degraded/unhealthy
    total = status.processed_count + status.error_count
    if total > 0:
        error_rate = status.error_count / total
        if error_rate > 0.15:
            return "UNHEALTHY"
        elif error_rate > 0.05:
            return "DEGRADED"
            
    return "HEALTHY"
