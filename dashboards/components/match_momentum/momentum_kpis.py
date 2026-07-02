"""Momentum KPI cards."""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from services.match_momentum_service import calculate_momentum_kpis


def render_momentum_kpis(events: list[dict[str, Any]]) -> None:
    """Render headline Match Momentum KPI cards."""
    st.subheader("Momentum KPIs")
    if not events:
        st.info("No event data available for momentum KPIs.")
        return

    kpis = calculate_momentum_kpis(events)
    if not kpis:
        st.info("No momentum KPI data calculated.")
        return

    cards = [
        ("Dominant Team", str(kpis.get("dominant_team", "N/A")), "#10b981"),
        ("Momentum Swings", str(kpis.get("momentum_swings", 0)), "#3b82f6"),
        ("Dangerous Attacks", str(kpis.get("dangerous_attacks", 0)), "#eab308"),
        ("Avg Possession Length", str(kpis.get("average_possession_length", 0.0)), "#ef4444"),
        ("Final Third Entries", str(kpis.get("final_third_entries", 0)), "#a855f7"),
        ("Progressive Actions", str(kpis.get("progressive_actions", 0)), "#14b8a6"),
    ]

    fig = go.Figure()
    slot_width = 1.0 / len(cards)
    for idx, (label, value, color) in enumerate(cards):
        x0 = idx * slot_width + 0.005
        x1 = (idx + 1) * slot_width - 0.005
        xc = (x0 + x1) / 2
        fig.add_shape(
            type="rect",
            xref="paper",
            yref="paper",
            x0=x0,
            x1=x1,
            y0=0.05,
            y1=0.95,
            line=dict(color="rgba(255, 255, 255, 0.2)", width=1),
            fillcolor="rgba(15, 23, 42, 0.55)",
        )
        fig.add_annotation(
            xref="paper",
            yref="paper",
            x=xc,
            y=0.68,
            text=value,
            showarrow=False,
            font=dict(color=color, size=20),
        )
        fig.add_annotation(
            xref="paper",
            yref="paper",
            x=xc,
            y=0.32,
            text=label,
            showarrow=False,
            font=dict(color="white", size=11),
        )

    fig.update_layout(
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[0, 1]),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=130,
    )

    st.plotly_chart(fig, use_container_width=True, key="match_momentum_kpis_plotly")