"""Metrics, throughput, lag, health status, and logging integration."""

from __future__ import annotations

from streaming.monitoring.pipeline_health import (
    register_monitored_pipeline,
    get_pipeline_status,
    get_pipeline_health,
)
from streaming.monitoring.stream_metrics import (
    calculate_stream_throughput,
    calculate_processing_latency,
    calculate_error_rate,
)
from streaming.monitoring.consumer_metrics import consumer_lag, consumer_rate
from streaming.monitoring.producer_metrics import producer_rate, producer_queue_size

__all__ = [
    "register_monitored_pipeline",
    "get_pipeline_status",
    "get_pipeline_health",
    "calculate_stream_throughput",
    "calculate_processing_latency",
    "calculate_error_rate",
    "consumer_lag",
    "consumer_rate",
    "producer_rate",
    "producer_queue_size",
]
