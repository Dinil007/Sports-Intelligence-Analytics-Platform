"""ETL Monitor Dashboard Component."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from services.monitoring_service import get_etl_monitoring, get_pipeline_status, get_scheduler_status, get_recent_job_runs

def render_etl_monitor() -> None:
    """Render ETL processing pipeline performance, scheduler status, and job logs."""
    st.markdown("### ⚙️ ETL & Pipelines Monitoring")
    etl = get_etl_monitoring()
    pipelines = get_pipeline_status()
    scheduler = get_scheduler_status()
    jobs = get_recent_job_runs()
    
    st.markdown(f"**ETL Subsystem Health:** `{etl['status']}` | **Active sync schedule routines:** `{scheduler['active_schedules_count']}` | **Next sync run:** `{scheduler['next_run_target']}`")
    
    c1, c2 = st.columns([1, 2])
    
    # Success rate gauge
    fig_succ = go.Figure(go.Indicator(
        mode="gauge+number",
        value=etl["success_rate_percent"],
        title={"text": "Pipeline Execution Success Rate", "font": {"color": "#f8fafc", "size": 14}},
        number={"suffix": "%", "font": {"color": "#f8fafc", "size": 22}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#64748b"},
            "bar": {"color": "#0ea5e9"},
            "bgcolor": "rgba(0,0,0,0)",
            "steps": [
                {"range": [0, 90], "color": "rgba(239,68,68,0.22)"},
                {"range": [90, 98], "color": "rgba(245,158,11,0.18)"},
                {"range": [98, 100], "color": "rgba(34,197,94,0.12)"},
            ]
        }
    ))
    fig_succ.update_layout(
        height=220, margin=dict(t=40, b=10, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0",
    )
    c1.plotly_chart(fig_succ, use_container_width=True, key="etl_success_gauge")
    
    # Pipelines status table
    c2.write("**Registered ETL Pipelines**")
    c2.dataframe(pd.DataFrame(pipelines), use_container_width=True, hide_index=True)
    
    st.markdown("#### Recent Job Run Logs")
    st.dataframe(pd.DataFrame(jobs), use_container_width=True, hide_index=True)
