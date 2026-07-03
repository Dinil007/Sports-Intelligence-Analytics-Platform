"""Budget planning rendering component."""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go # type: ignore
from services.executive_bi_service import calculate_budget_plan

def render_budget_planning() -> None:
    """Render budget allocation pie chart."""
    data = calculate_budget_plan()
    
    fig = go.Figure(data=[go.Pie(
        labels=data["departments"],
        values=data["allocations"],
        marker=dict(colors=["#00CCFF", "#CC00FF", "#FFCC00", "#FF4B4B", "#00FFCC"])
    )])
    
    fig.update_layout(
        title="Squad & Infrastructure Budget Allocation",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
    )
    
    st.plotly_chart(fig, use_container_width=True)
