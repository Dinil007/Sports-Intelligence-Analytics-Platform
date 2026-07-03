"""Merchandise sales rendering component."""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go # type: ignore
from services.executive_bi_service import calculate_merchandise_sales

def render_merchandise_sales() -> None:
    """Render quarterly merchandise category revenue trends as line charts."""
    data = calculate_merchandise_sales()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["quarters"],
        y=[val / 1e6 for val in data["jersey_sales"]],
        mode="lines+markers",
        name="Jersey Sales (€M)",
        line=dict(color="#00FFCC", width=3)
    ))
    fig.add_trace(go.Scatter(
        x=data["quarters"],
        y=[val / 1e6 for val in data["accessories"]],
        mode="lines+markers",
        name="Accessories & Fashion (€M)",
        line=dict(color="#FF3366", width=2, dash="dash")
    ))
    
    fig.update_layout(
        title="Quarterly Merchandise Revenue Trends by Category",
        xaxis_title="Quarter Sequence",
        yaxis_title="Revenue (€M)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        xaxis=dict(gridcolor="#333333"),
        yaxis=dict(gridcolor="#333333"),
    )
    
    st.plotly_chart(fig, use_container_width=True)
