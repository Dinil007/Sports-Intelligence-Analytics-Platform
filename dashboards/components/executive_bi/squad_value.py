"""Squad valuation rendering component."""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go # type: ignore
from services.executive_bi_service import calculate_squad_value

def render_squad_value() -> None:
    """Render squad market value distribution bar chart across positions."""
    data = calculate_squad_value()
    
    fig = go.Figure(data=[go.Bar(
        x=data["positions"],
        y=[val / 1e6 for val in data["values"]],
        marker_color="#00FFCC"
    )])
    
    fig.update_layout(
        title="Asset Valuation by Position Tier (€M)",
        xaxis_title="Position Group",
        yaxis_title="Market Value (€M)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        xaxis=dict(gridcolor="#333333"),
        yaxis=dict(gridcolor="#333333"),
    )
    
    st.plotly_chart(fig, use_container_width=True)
