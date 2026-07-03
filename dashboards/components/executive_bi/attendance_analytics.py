"""Attendance trends rendering component."""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go # type: ignore
from services.executive_bi_service import calculate_attendance

def render_attendance_analytics() -> None:
    """Render home matches stadium attendance trend line chart."""
    data = calculate_attendance()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["matches"],
        y=data["attendance_pct"],
        mode="lines+markers",
        name="Stadium Attendance (%)",
        line=dict(color="#FFD700", width=3)
    ))
    
    fig.update_layout(
        title="Home Match Stadium Attendance Rate Trends",
        xaxis_title="Matchday Sequence",
        yaxis_title="Attendance Rate (%)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        xaxis=dict(gridcolor="#333333"),
        yaxis=dict(gridcolor="#333333"),
        yaxis_range=[80, 100],
    )
    
    st.plotly_chart(fig, use_container_width=True)
