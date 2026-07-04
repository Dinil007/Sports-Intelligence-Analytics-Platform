"""Orchestrator for the Observability & Monitoring dashboard."""
from __future__ import annotations

import streamlit as st

from dashboards.components.monitoring.system_health import render_system_health
from dashboards.components.monitoring.resource_usage import render_resource_usage
from dashboards.components.monitoring.service_status import render_service_status
from dashboards.components.monitoring.api_monitor import render_api_monitor
from dashboards.components.monitoring.database_monitor import render_database_monitor
from dashboards.components.monitoring.streaming_monitor import render_streaming_monitor
from dashboards.components.monitoring.ml_monitor import render_ml_monitor
from dashboards.components.monitoring.etl_monitor import render_etl_monitor
from dashboards.components.monitoring.authentication_monitor import render_authentication_monitor
from dashboards.components.monitoring.alert_center import render_alert_center
from dashboards.components.monitoring.audit_logs import render_audit_logs
from dashboards.components.monitoring.performance_dashboard import render_performance_dashboard
from dashboards.components.monitoring.monitoring_summary import render_monitoring_summary


def render_monitoring_dashboard() -> None:
    """Render the master Observability & Monitoring dashboard."""
    st.title("📈 Observability & Monitoring Platform")
    st.markdown("---")

    # 1. System Health
    render_system_health()
    st.markdown("---")

    # 2. Resource Usage
    render_resource_usage()
    st.markdown("---")

    # 3. Service Status
    render_service_status()
    st.markdown("---")

    # 4. API Monitoring
    render_api_monitor()
    st.markdown("---")

    # 5. Database Monitoring
    render_database_monitor()
    st.markdown("---")

    # 6. Streaming Monitoring
    render_streaming_monitor()
    st.markdown("---")

    # 7. ML Monitoring
    render_ml_monitor()
    st.markdown("---")

    # 8. ETL Monitoring
    render_etl_monitor()
    st.markdown("---")

    # 9. Authentication Monitoring
    render_authentication_monitor()
    st.markdown("---")

    # 10. Alert Center
    render_alert_center()
    st.markdown("---")

    # 11. Audit Logs
    render_audit_logs()
    st.markdown("---")

    # 12. Performance Dashboard
    render_performance_dashboard()
    st.markdown("---")

    # 13. Executive Monitoring Summary
    render_monitoring_summary()
