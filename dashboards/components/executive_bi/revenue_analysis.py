"""Revenue streams rendering component."""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go # type: ignore
from services.executive_bi_service import calculate_revenue_analysis

def render_revenue_analysis() -> None:
    """Render revenue streams breakdown donut chart."""
    data = calculate_revenue_analysis()
    
    fig = go.Figure(data=[go.Pie(
        labels=data["categories"],
        values=data["values"],
        hole=0.4,
        marker=dict(colors=["#00FFCC", "#00CCFF", "#CC00FF", "#FFCC00", "#FF4B4B"])
    )])
    
    fig.update_layout(
        title="Revenue Stream Breakdown",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
    )
    
    st.plotly_chart(fig, use_container_width=True)
