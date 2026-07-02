"""Ball progression chart."""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from services.match_momentum_service import calculate_ball_progression


def render_ball_progression(events: list[dict[str, Any]]) -> None:
    """Render cumulative progressive pass and carry distance."""
    st.subheader("Ball Progression")
    if not events:
        st.info("No event data available for ball progression.")
        return

    progression = calculate_ball_progression(events)
    minutes = progression.get("minutes", [])
    teams = progression.get("teams", {})
    if not minutes or not teams:
        st.info("No ball progression data calculated.")
        return

    fig = go.Figure()
    colors = ["#14b8a6", "#a855f7", "#eab308", "#3b82f6"]
    for idx, (team, values) in enumerate(teams.items()):
        fig.add_trace(
            go.Scatter(
                x=minutes,
                y=values,
                mode="lines",
                name=team,
                line=dict(color=colors[idx % len(colors)], width=3),
                hovertemplate="Minute: %{x}<br>Cumulative Progression: %{y}m<extra>" + team + "</extra>",
            )
        )

    fig.update_layout(
        title_text="Cumulative Ball Progression",
        xaxis_title="Match Minute",
        yaxis_title="Progression Distance",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color="white"),
        legend=dict(font=dict(color="white"), orientation="h", y=1.08),
        margin=dict(l=40, r=20, t=60, b=50),
        height=340,
    )
    fig.update_xaxes(gridcolor="rgba(255, 255, 255, 0.1)")
    fig.update_yaxes(gridcolor="rgba(255, 255, 255, 0.1)")

    st.plotly_chart(fig, use_container_width=True, key="match_momentum_ball_progression_plotly")
