"""Observability and monitoring configuration."""
from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MONITORING_DIR = PROJECT_ROOT / "data" / "monitoring"

# Ensure data directory exists
MONITORING_DIR.mkdir(parents=True, exist_ok=True)

class MonitoringConfig:
    """Config settings for Observability platform."""
    STORAGE_DIR: Path = MONITORING_DIR
    SYSTEM_METRICS_PATH: Path = MONITORING_DIR / "system_metrics.json"
    API_METRICS_PATH: Path = MONITORING_DIR / "api_metrics.json"
    DATABASE_METRICS_PATH: Path = MONITORING_DIR / "database_metrics.json"
    STREAMING_METRICS_PATH: Path = MONITORING_DIR / "streaming_metrics.json"
    ML_METRICS_PATH: Path = MONITORING_DIR / "ml_metrics.json"
    ETL_METRICS_PATH: Path = MONITORING_DIR / "etl_metrics.json"
    AUTH_METRICS_PATH: Path = MONITORING_DIR / "auth_metrics.json"
    ALERTS_PATH: Path = MONITORING_DIR / "alerts.json"
    AUDIT_LOG_PATH: Path = MONITORING_DIR / "audit_log.json"
