"""Player ROI rendering component."""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go # type: ignore
from services.executive_bi_service import calculate_player_roi

def render_player_roi() -> None:
    """Render player transfer acquisition ROI scatter plot."""
    data = calculate_player_roi()
    
    fig = go.Figure(data=[go.Scatter(
        x=data["purchase_fees"],
        y=data["performance_index"],
        mode="markers+text",
        text=data["players"],
        textposition="top center",
        marker=dict(
            size=[roi * 15 for roi in data["roi_factor"]],
            color=data["roi_factor"],
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(title="ROI Factor")
        )
    )])
    
    fig.update_layout(
        title="Player Acquisition Cost vs Performance Index (Bubble Size = ROI)",
        xaxis_title="Purchase Fee (€M)",
        yaxis_title="Sporta Performance Index",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        xaxis=dict(gridcolor="#333333"),
        yaxis=dict(gridcolor="#333333"),
    )
    
    st.plotly_chart(fig, use_container_width=True)
