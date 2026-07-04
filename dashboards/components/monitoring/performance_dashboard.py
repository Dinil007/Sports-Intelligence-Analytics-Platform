"""Performance Dashboard Component."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st
from services.monitoring_service import get_api_statistics

def render_performance_dashboard() -> None:
    """Render performance trends line charts."""
    st.markdown("### 📈 Overall Performance Dashboard")
    stats = get_api_statistics()
    
    # Combined latency line chart
    df = pd.DataFrame(stats["latency_trends"])
    fig = px.line(
        df, x="hour", y="latency_ms",
        title="Inference & API Response Time Latency Trends (ms)",
        color_discrete_sequence=["#a78bfa"],
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0", title_font_color="#f8fafc",
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.12)"),
    )
    st.plotly_chart(fig, use_container_width=True, key="perf_latency_line")
