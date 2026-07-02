"""Dangerous attacks chart."""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from services.match_momentum_service import calculate_dangerous_attacks


def render_dangerous_attacks(events: list[dict[str, Any]]) -> None:
    """Render dangerous attacks by team as grouped horizontal bars."""
    st.subheader("Dangerous Attacks")
    if not events:
        st.info("No event data available for dangerous attacks.")
        return

    attacks = calculate_dangerous_attacks(events)
    if not attacks:
        st.info("No dangerous attacks calculated.")
        return

    fig = go.Figure()
    colors = ["#ef4444", "#3b82f6", "#10b981", "#eab308"]
    for idx, (team, count) in enumerate(attacks.items()):
        fig.add_trace(
            go.Bar(
                y=["Dangerous Attacks"],
                x=[count],
                name=team,
                orientation="h",
                marker=dict(color=colors[idx % len(colors)], line=dict(color="white", width=1)),
                text=[count],
                textposition="auto",
                hovertemplate="Team: " + team + "<br>Dangerous Attacks: %{x}<extra></extra>",
            )
        )

    fig.update_layout(
        title_text="Dangerous Attacks by Team",
        xaxis_title="Dangerous Attacks",
        barmode="group",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color="white"),
        legend=dict(font=dict(color="white"), orientation="h", y=1.1),
        margin=dict(l=140, r=20, t=60, b=50),
        height=260,
    )
    fig.update_xaxes(gridcolor="rgba(255, 255, 255, 0.1)")

    st.plotly_chart(fig, use_container_width=True, key="match_momentum_dangerous_attacks_plotly")
