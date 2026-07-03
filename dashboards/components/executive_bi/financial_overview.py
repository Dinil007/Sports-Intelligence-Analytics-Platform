"""Financial Overview rendering component."""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go # type: ignore
from services.executive_bi_service import calculate_financial_overview

def render_financial_overview() -> None:
    """Render financial trend line charts (Revenue vs Expenses vs Profit)."""
    data = calculate_financial_overview()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["months"], y=data["revenue_trend"],
        mode="lines+markers", name="Revenue (€M)",
        line=dict(color="#00FFCC", width=3)
    ))
    fig.add_trace(go.Scatter(
        x=data["months"], y=data["expense_trend"],
        mode="lines+markers", name="Expenses (€M)",
        line=dict(color="#FF4B4B", width=3)
    ))
    fig.add_trace(go.Scatter(
        x=data["months"], y=data["profit_trend"],
        mode="lines+markers", name="Profit (€M)",
        line=dict(color="#FFA500", width=2, dash="dash")
    ))
    
    fig.update_layout(
        title="Revenue, Expense & Profit Trends (Monthly)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        xaxis=dict(gridcolor="#333333"),
        yaxis=dict(gridcolor="#333333"),
    )
    
    st.plotly_chart(fig, use_container_width=True)
