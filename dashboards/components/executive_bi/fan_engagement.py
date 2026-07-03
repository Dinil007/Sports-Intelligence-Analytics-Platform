"""Fan engagement rendering component."""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go # type: ignore
from services.executive_bi_service import calculate_fan_engagement

def render_fan_engagement() -> None:
    """Render monthly fan engagement/membership trends as an Area Chart."""
    data = calculate_fan_engagement()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["months"],
        y=data["social_reach"],
        mode="lines",
        fill="tozeroy",
        name="Social Reach (M)",
        line=dict(color="#00CCFF", width=2)
    ))
    
    fig.update_layout(
        title="Fan Engagement Trends - Total Social Media Reach",
        xaxis_title="Month",
        yaxis_title="Impressions / Reach (Millions)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        xaxis=dict(gridcolor="#333333"),
        yaxis=dict(gridcolor="#333333"),
    )
    
    st.plotly_chart(fig, use_container_width=True)
