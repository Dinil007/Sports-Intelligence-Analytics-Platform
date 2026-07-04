"""Monitoring Summary — high-level KPI cards."""
from __future__ import annotations

import streamlit as st
from services.monitoring_service import generate_monitoring_summary
from monitoring.constants import STATUS_HEALTHY, STATUS_WARNING, STATUS_CRITICAL

_STATUS_COLORS = {
    STATUS_HEALTHY:  "#22c55e",
    STATUS_WARNING:  "#f59e0b",
    STATUS_CRITICAL: "#ef4444",
    "Offline":       "#64748b",
    "Degraded":      "#8b5cf6",
}

def _badge(label: str, value: str, color: str) -> str:
    return (
        f'<div style="background:rgba(15,23,42,0.9);border:1px solid {color}44;'
        f'border-radius:14px;padding:1rem 1.2rem;text-align:center;'
        f'box-shadow:0 4px 24px rgba(0,0,0,0.22)">'
        f'<div style="color:{color};font-size:1.6rem;font-weight:900">{value}</div>'
        f'<div style="color:#94a3b8;font-size:0.78rem;margin-top:.3rem">{label}</div>'
        f'</div>'
    )

def render_monitoring_summary() -> None:
    """Render top-level KPI summary cards."""
    st.markdown("### 📊 Executive Monitoring Summary")
    summary = generate_monitoring_summary()

    cols = st.columns(4)
    items = [
        ("System", summary["system_status"]),
        ("API",    summary["api_status"]),
        ("Database", summary["database_status"]),
        ("Streaming", summary["streaming_status"]),
    ]
    for col, (label, status) in zip(cols, items):
        color = _STATUS_COLORS.get(status, "#64748b")
        col.markdown(_badge(label, status, color), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("⚠️ Warning Alerts",  summary["warning_alerts_count"])
    c2.metric("🔴 Critical Alerts", summary["critical_alerts_count"])
    c3.metric("⏱ Uptime",          summary["uptime"])
