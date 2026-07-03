"""Sponsorship portfolio rendering component."""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go # type: ignore
from services.executive_bi_service import calculate_sponsorship_metrics

def render_sponsorship_analysis() -> None:
    """Render sponsorship contract revenue distribution bar chart."""
    data = calculate_sponsorship_metrics()
    
    fig = go.Figure(data=[go.Bar(
        x=data["sponsors"],
        y=[rev / 1e6 for rev in data["revenue"]],
        marker_color="#CC00FF"
    )])
    
    fig.update_layout(
        title="Commercial Sponsorship Portfolio Revenue (€M)",
        xaxis_title="Sponsor Tier",
        yaxis_title="Annual Value (€M)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        xaxis=dict(gridcolor="#333333"),
        yaxis=dict(gridcolor="#333333"),
    )
    
    st.plotly_chart(fig, use_container_width=True)
