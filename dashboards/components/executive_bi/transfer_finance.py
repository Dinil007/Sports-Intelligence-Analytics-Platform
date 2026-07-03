"""Transfer finance trends rendering component."""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go # type: ignore
from services.executive_bi_service import calculate_transfer_finance

def render_transfer_finance() -> None:
    """Render historical transfer spending vs income bar chart."""
    data = calculate_transfer_finance()
    
    fig = go.Figure(data=[
        go.Bar(name="Spending (€M)", x=data["seasons"], y=data["spending"], marker_color="#FF4B4B"),
        go.Bar(name="Income (€M)", x=data["seasons"], y=data["income"], marker_color="#00FFCC")
    ])
    
    fig.update_layout(
        barmode="group",
        title="Transfer Expenditure vs Income by Season",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        xaxis=dict(gridcolor="#333333"),
        yaxis=dict(gridcolor="#333333"),
    )
    
    st.plotly_chart(fig, use_container_width=True)
