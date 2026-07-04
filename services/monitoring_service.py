"""Observability & Monitoring Service layer.

Provides unified entrypoint for accessing all platform monitoring metrics.
"""
from __future__ import annotations

from typing import Dict, Any, List

# System monitors
from monitoring.system.system_health import check_system_health
from monitoring.system.resource_monitor import get_cpu_status, get_memory_status, get_disk_status
from monitoring.system.service_status import check_services_status
from monitoring.system.uptime_monitor import get_uptime_status

# API monitors
from monitoring.api.api_monitor import check_api_health
from monitoring.api.request_monitor import get_request_trends, get_request_volume
from monitoring.api.response_monitor import get_latency_trends, get_p95_latency, get_error_rate
from monitoring.api.endpoint_statistics import get_top_endpoints

# Database monitors
from monitoring.database.database_monitor import check_database_health
from monitoring.database.connection_monitor import get_active_connections, get_connection_history
from monitoring.database.storage_monitor import get_db_size_gb
from monitoring.database.query_monitor import get_slow_queries

# Streaming monitors
from monitoring.streaming.stream_monitor import check_streaming_health
from monitoring.streaming.kafka_monitor import get_broker_status, get_throughput_history
from monitoring.streaming.consumer_monitor import get_consumers_status, get_consumer_lag_trends
from monitoring.streaming.producer_monitor import get_producers_status

# ML monitors
from monitoring.ml.prediction_monitor import get_prediction_stats, get_prediction_throughput_trends
from monitoring.ml.model_monitor import check_models_status
from monitoring.ml.drift_monitor import get_drift_metrics
from monitoring.ml.training_monitor import get_training_metrics

# ETL monitors
from monitoring.etl.etl_monitor import check_etl_health
from monitoring.etl.job_monitor import get_recent_job_runs
from monitoring.etl.pipeline_monitor import get_pipelines_status
from monitoring.etl.scheduler_monitor import get_scheduler_status as scheduler_status_impl

# Authentication monitors
from monitoring.authentication.login_monitor import (
    get_login_statistics as login_stats_impl,
    get_login_trends as login_trends_impl,
)
from monitoring.authentication.session_monitor import (
    get_session_statistics as session_stats_impl,
    get_session_trends as session_trends_impl,
)
from monitoring.authentication.security_monitor import get_security_events

# Alerts
from monitoring.alerts.alert_engine import run_alert_rules
from monitoring.alerts.alert_manager import get_active_alerts

# Audit
from monitoring.audit.audit_logger import fetch_audit_logs


def get_system_health() -> Dict[str, Any]:
    """Returns aggregated status and health parameters of the system."""
    return check_system_health()


def get_resource_usage() -> Dict[str, Any]:
    """Returns combined resource usage metrics."""
    return {
        "cpu": get_cpu_status(),
        "memory": get_memory_status(),
        "disk": get_disk_status(),
        "uptime": get_uptime_status(),
    }


def get_cpu_usage() -> Dict[str, Any]:
    """Returns CPU status."""
    return get_cpu_status()


def get_memory_usage() -> Dict[str, Any]:
    """Returns Memory status."""
    return get_memory_status()


def get_disk_usage() -> Dict[str, Any]:
    """Returns Disk status."""
    return get_disk_status()


def get_service_status() -> List[Dict[str, Any]]:
    """Returns status check of platform dependencies."""
    return check_services_status()


def get_api_statistics() -> Dict[str, Any]:
    """Returns overall API metrics and trends."""
    return {
        "health": check_api_health(),
        "volume_trends": get_request_trends(),
        "latency_trends": get_latency_trends(),
    }


def get_endpoint_metrics() -> List[Dict[str, Any]]:
    """Returns metrics grouped by individual endpoints."""
    return get_top_endpoints()


def get_database_health() -> Dict[str, Any]:
    """Returns database health indicators."""
    return check_database_health()


def get_database_connections() -> Dict[str, Any]:
    """Returns DB active connection count and trends."""
    return {
        "active": get_active_connections(),
        "history": get_connection_history(),
        "slow_queries": get_slow_queries(),
    }


def get_database_storage() -> Dict[str, Any]:
    """Returns database disk usage size."""
    return {
        "size_gb": get_db_size_gb(),
    }


def get_streaming_health() -> Dict[str, Any]:
    """Returns Kafka streaming health."""
    return check_streaming_health()


def get_kafka_metrics() -> Dict[str, Any]:
    """Returns broker metrics and trends."""
    return {
        "broker": get_broker_status(),
        "throughput_history": get_throughput_history(),
    }


def get_consumer_metrics() -> Dict[str, Any]:
    """Returns consumer group status and lag trends."""
    return {
        "groups": get_consumers_status(),
        "lag_trends": get_consumer_lag_trends(),
    }


def get_producer_metrics() -> List[Dict[str, Any]]:
    """Returns producer metrics."""
    return get_producers_status()


def get_ml_monitoring() -> Dict[str, Any]:
    """Returns combined ML observability metrics."""
    return {
        "predictions": get_prediction_stats(),
        "models": check_models_status(),
        "drift": get_drift_metrics(),
        "training": get_training_metrics(),
    }


def get_prediction_statistics() -> Dict[str, Any]:
    """Returns live serving serving stats."""
    return {
        "stats": get_prediction_stats(),
        "throughput_trends": get_prediction_throughput_trends(),
    }


def get_model_status() -> List[Dict[str, Any]]:
    """Returns status details of all deployed models."""
    return check_models_status()


def get_drift_status() -> Dict[str, Any]:
    """Returns drift scores."""
    return get_drift_metrics()


def get_etl_monitoring() -> Dict[str, Any]:
    """Returns ETL health metrics."""
    return check_etl_health()


def get_pipeline_status() -> List[Dict[str, Any]]:
    """Returns list of pipeline executions."""
    return get_pipelines_status()


def get_scheduler_status() -> Dict[str, Any]:
    """Returns status of sync schedules scheduler."""
    return scheduler_status_impl()


def get_authentication_statistics() -> Dict[str, Any]:
    """Returns combined authentication security stats."""
    return {
        "login": login_stats_impl(),
        "sessions": session_stats_impl(),
        "security_events": get_security_events(),
    }


def get_login_statistics() -> Dict[str, Any]:
    """Returns login statistics and history."""
    return {
        "stats": login_stats_impl(),
        "trends": login_trends_impl(),
    }


def get_session_statistics() -> Dict[str, Any]:
    """Returns active session statistics."""
    return {
        "stats": session_stats_impl(),
        "trends": session_trends_impl(),
    }


def generate_alerts() -> List[Dict[str, Any]]:
    """Forces evaluating threshold rules and returns active issues."""
    return run_alert_rules()


def list_active_alerts() -> List[Dict[str, Any]]:
    """Returns raised active warnings/critical issues."""
    return get_active_alerts()


def get_audit_logs() -> List[Dict[str, Any]]:
    """Returns chronological audit timeline events."""
    return fetch_audit_logs()


def generate_monitoring_summary() -> Dict[str, Any]:
    """Aggregates all components into high-level dashboard metrics summary."""
    sys_status = check_system_health()["status"]
    api_status = check_api_health()["status"]
    db_status = check_database_health()["status"]
    stream_status = check_streaming_health()["status"]
    etl_status = check_etl_health()["status"]
    
    active_alerts = get_active_alerts()
    critical_count = sum(1 for a in active_alerts if a["level"] == "CRITICAL")
    warning_count = sum(1 for a in active_alerts if a["level"] == "WARNING")
    
    return {
        "system_status": sys_status,
        "api_status": api_status,
        "database_status": db_status,
        "streaming_status": stream_status,
        "etl_status": etl_status,
        "critical_alerts_count": critical_count,
        "warning_alerts_count": warning_count,
        "uptime": get_uptime_status()["formatted"],
    }
