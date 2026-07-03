"""Throughput, processing latency, and error rate monitoring."""

from __future__ import annotations

from typing import Dict, Any
from streaming.monitoring.pipeline_health import _ACTIVE_PIPELINES

def calculate_stream_throughput(pipeline_id: str = "live-football-ingest") -> float:
    """Return average processed messages per second since start."""
    manager = _ACTIVE_PIPELINES.get(pipeline_id)
    if not manager or not manager.start_time:
        return 0.0
    status = manager.get_status()
    if status.uptime_seconds <= 0.0:
        return 0.0
    return round(status.processed_count / status.uptime_seconds, 2)

def calculate_processing_latency(pipeline_id: str = "live-football-ingest") -> float:
    """Return average latency of event processing in milliseconds."""
    manager = _ACTIVE_PIPELINES.get(pipeline_id)
    if not manager or not manager.latencies:
        return 0.0
    avg_sec = sum(manager.latencies) / len(manager.latencies)
    return round(avg_sec * 1000.0, 2)  # return in ms

def calculate_error_rate(pipeline_id: str = "live-football-ingest") -> float:
    """Return fraction of processing runs that failed validation or load."""
    manager = _ACTIVE_PIPELINES.get(pipeline_id)
    if not manager:
        return 0.0
    status = manager.get_status()
    total = status.processed_count + status.error_count
    if total <= 0:
        return 0.0
    return round((status.error_count / total) * 100.0, 2)
