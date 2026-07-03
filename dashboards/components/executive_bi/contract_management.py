"""Contract management rendering component."""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go # type: ignore
from services.executive_bi_service import calculate_contract_status

def render_contract_management() -> None:
    """Render player contract expiry risk horizon chart."""
    data = calculate_contract_status()
    
    fig = go.Figure(data=[go.Bar(
        x=data["expiries"],
        y=data["counts"],
        marker_color=["#FF4B4B", "#FFA500", "#FFD700", "#00FF7F", "#1E90FF"]
    )])
    
    fig.update_layout(
        title="Contract Expiry Horizon (Upcoming Years)",
        xaxis_title="Expiry Year",
        yaxis_title="Number of Players",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        xaxis=dict(gridcolor="#333333"),
        yaxis=dict(gridcolor="#333333"),
    )
    
    st.plotly_chart(fig, use_container_width=True)
