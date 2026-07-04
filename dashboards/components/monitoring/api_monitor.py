"""API Monitor Dashboard Component."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st
from services.monitoring_service import get_api_statistics, get_endpoint_metrics

def render_api_monitor() -> None:
    """Render API response times, volume, and endpoints."""
    st.markdown("### 🌐 API Monitoring")
    stats = get_api_statistics()
    endpoints = get_endpoint_metrics()
    
    health = stats["health"]
    st.markdown(f"**API Gateway Health:** `{health['status']}` | **24h Request Volume:** `{health['request_volume']}` | **Error Rate:** `{health['error_rate_percent']}%` | **p95 Latency:** `{health['p95_latency_ms']} ms` ")
    
    c1, c2 = st.columns(2)
    
    # Request volume line chart
    df_vol = pd.DataFrame(stats["volume_trends"])
    fig_vol = px.line(
        df_vol, x="hour", y="requests",
        title="Hourly Request Volume",
        color_discrete_sequence=["#38bdf8"],
    )
    fig_vol.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0", title_font_color="#f8fafc",
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.12)"),
    )
    c1.plotly_chart(fig_vol, use_container_width=True, key="api_requests_line")
    
    # Response time Area chart
    df_lat = pd.DataFrame(stats["latency_trends"])
    fig_lat = px.area(
        df_lat, x="hour", y="latency_ms",
        title="Hourly Latency Trends (ms)",
        color_discrete_sequence=["#a78bfa"],
    )
    fig_lat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0", title_font_color="#f8fafc",
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.12)"),
    )
    c2.plotly_chart(fig_lat, use_container_width=True, key="api_latency_area")
    
    # Endpoint statistics Bar chart
    st.markdown("#### Endpoint Usage Statistics")
    df_end = pd.DataFrame(endpoints)
    fig_end = px.bar(
        df_end, x="endpoint", y="calls",
        title="Top Endpoint Calls Count",
        color="avg_latency_ms",
        color_continuous_scale=px.colors.sequential.Purples,
    )
    fig_end.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0", title_font_color="#f8fafc",
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.12)"),
    )
    st.plotly_chart(fig_end, use_container_width=True, key="api_endpoints_bar")
    st.dataframe(df_end, use_container_width=True, hide_index=True)
