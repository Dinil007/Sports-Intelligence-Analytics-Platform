"""System health gauges — CPU, Memory, Disk."""
from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st
from services.monitoring_service import get_system_health

_GAUGE_COLORS = ["#22c55e", "#f59e0b", "#ef4444"]

def _gauge(title: str, value: float, max_val: float = 100.0) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"color": "#f8fafc", "size": 14}},
        number={"suffix": "%", "font": {"color": "#f8fafc", "size": 22}},
        gauge={
            "axis": {"range": [0, max_val], "tickcolor": "#64748b"},
            "bar": {"color": "#38bdf8"},
            "bgcolor": "rgba(0,0,0,0)",
            "steps": [
                {"range": [0, 80],  "color": "rgba(34,197,94,0.12)"},
                {"range": [80, 90], "color": "rgba(245,158,11,0.18)"},
                {"range": [90, 100],"color": "rgba(239,68,68,0.22)"},
            ],
            "threshold": {
                "line": {"color": "#ef4444", "width": 3},
                "thickness": 0.75,
                "value": 90,
            },
        },
    ))
    fig.update_layout(
        height=220, margin=dict(t=40, b=10, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0",
    )
    return fig

def render_system_health() -> None:
    """Render CPU, Memory, Disk gauges."""
    st.markdown("### 🖥 System Health")
    health = get_system_health()
    cpu  = health["cpu"]
    mem  = health["memory"]
    disk = health["disk"]

    c1, c2, c3 = st.columns(3)
    c1.plotly_chart(_gauge("CPU Usage", cpu["percentage"]),   use_container_width=True, key="sys_cpu_gauge")
    c2.plotly_chart(_gauge("Memory Usage", mem["percentage"]), use_container_width=True, key="sys_mem_gauge")
    c3.plotly_chart(_gauge("Disk Usage", disk["percentage"]), use_container_width=True, key="sys_disk_gauge")

    with st.expander("Resource Details"):
        d1, d2 = st.columns(2)
        d1.write(f"**Memory:** {mem['used_gb']} GB / {mem['total_gb']} GB")
        d2.write(f"**Disk:** {disk['used_gb']} GB / {disk['total_gb']} GB")
