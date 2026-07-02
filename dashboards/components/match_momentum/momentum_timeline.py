"""Momentum timeline chart."""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from services.match_momentum_service import calculate_match_momentum


def render_momentum_timeline(events: list[dict[str, Any]]) -> None:
    """Render weighted match momentum over time."""
    st.subheader("Momentum Timeline")
    if not events:
        st.info("No event data available for momentum timeline.")
        return

    momentum = calculate_match_momentum(events)
    minutes = momentum.get("minutes", [])
    teams = momentum.get("teams", {})
    if not minutes or not teams:
        st.info("No momentum data calculated.")
        return

    fig = go.Figure()
    colors = ["#10b981", "#3b82f6", "#eab308", "#a855f7"]
    for idx, (team, values) in enumerate(teams.items()):
        fig.add_trace(
            go.Scatter(
                x=minutes,
                y=values,
                mode="lines",
                name=team,
                line=dict(color=colors[idx % len(colors)], width=3),
                hovertemplate="Minute: %{x}<br>Momentum: %{y}<extra>" + team + "</extra>",
            )
        )

    fig.update_layout(
        title_text="Match Momentum",
        xaxis_title="Match Minute",
        yaxis_title="Momentum Score",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color="white"),
        legend=dict(font=dict(color="white"), orientation="h", y=1.08),
        margin=dict(l=40, r=20, t=60, b=50),
        height=360,
    )
    fig.update_xaxes(gridcolor="rgba(255, 255, 255, 0.1)")
    fig.update_yaxes(gridcolor="rgba(255, 255, 255, 0.1)")

    st.plotly_chart(fig, use_container_width=True, key="match_momentum_timeline_plotly")
