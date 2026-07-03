"""Expense breakdown rendering component."""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go # type: ignore
from services.executive_bi_service import calculate_expense_analysis

def render_expense_analysis() -> None:
    """Render expense breakdown donut chart."""
    data = calculate_expense_analysis()
    
    fig = go.Figure(data=[go.Pie(
        labels=data["categories"],
        values=data["values"],
        hole=0.4,
        marker=dict(colors=["#FF4B4B", "#FFA500", "#FFD700", "#00FF7F", "#40E0D0", "#1E90FF"])
    )])
    
    fig.update_layout(
        title="Expense Allocation Breakdown",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
    )
    
    st.plotly_chart(fig, use_container_width=True)
