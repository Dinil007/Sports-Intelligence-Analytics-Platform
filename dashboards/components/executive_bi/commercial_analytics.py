"""Commercial Analytics overview rendering component."""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go # type: ignore
from services.executive_bi_service import calculate_sponsorship_metrics, calculate_merchandise_sales

def render_commercial_analytics() -> None:
    """Render high-level commercial portfolio overview chart."""
    sponsorship = calculate_sponsorship_metrics()
    merch = calculate_merchandise_sales()
    
    total_sponsor = sum(sponsorship["revenue"])
    total_merch = sum(merch["jersey_sales"]) + sum(merch["accessories"])
    
    fig = go.Figure(data=[
        go.Bar(
            x=["Sponsorship Portfolio", "Merchandise Sales"],
            y=[total_sponsor / 1e6, total_merch / 1e6],
            marker_color=["#00CCFF", "#CC00FF"]
        )
    ])
    
    fig.update_layout(
        title="Commercial Portfolios - Sponsorship vs Merchandise (€M)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        xaxis=dict(gridcolor="#333333"),
        yaxis=dict(gridcolor="#333333"),
    )
    
    st.plotly_chart(fig, use_container_width=True)
