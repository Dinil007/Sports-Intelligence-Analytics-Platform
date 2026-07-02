"""Possession flow chart."""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from services.match_momentum_service import calculate_possession_flow


def render_possession_flow(events: list[dict[str, Any]]) -> None:
    """Render possession share over match time as a stacked area chart."""
    st.subheader("Possession Flow")
    if not events:
        st.info("No event data available for possession flow.")
        return

    flow = calculate_possession_flow(events)
    minutes = flow.get("minutes", [])
    teams = flow.get("teams", {})
    if not minutes or not teams:
        st.info("No possession flow data calculated.")
        return

    fig = go.Figure()
    colors = ["#10b981", "#3b82f6", "#eab308", "#a855f7"]
    for idx, (team, values) in enumerate(teams.items()):
        fig.add_trace(
            go.Scatter(
                x=minutes,
                y=values,
                mode="lines",
                stackgroup="one",
                name=team,
                line=dict(color=colors[idx % len(colors)], width=1),
                hovertemplate="Minute: %{x}<br>Possession: %{y}%<extra>" + team + "</extra>",
            )
        )

    fig.update_layout(
        title_text="Possession Flow Over Time",
        xaxis_title="Match Minute",
        yaxis_title="Possession Share (%)",
        yaxis_range=[0, 100],
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color="white"),
        legend=dict(font=dict(color="white"), orientation="h", y=1.08),
        margin=dict(l=40, r=20, t=60, b=50),
        height=340,
    )
    fig.update_xaxes(gridcolor="rgba(255, 255, 255, 0.1)")
    fig.update_yaxes(gridcolor="rgba(255, 255, 255, 0.1)")

    st.plotly_chart(fig, use_container_width=True, key="match_momentum_possession_flow_plotly")
