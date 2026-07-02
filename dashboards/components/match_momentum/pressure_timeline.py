"""Pressure timeline chart."""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from services.match_momentum_service import calculate_pressure_timeline


def render_pressure_timeline(events: list[dict[str, Any]]) -> None:
    """Render pressure events by minute."""
    st.subheader("Pressure Timeline")
    if not events:
        st.info("No event data available for pressure timeline.")
        return

    pressure = calculate_pressure_timeline(events)
    minutes = pressure.get("minutes", [])
    teams = pressure.get("teams", {})
    if not minutes or not teams:
        st.info("No pressure timeline data calculated.")
        return

    fig = go.Figure()
    colors = ["#ef4444", "#3b82f6", "#10b981", "#eab308"]
    for idx, (team, values) in enumerate(teams.items()):
        fig.add_trace(
            go.Scatter(
                x=minutes,
                y=values,
                mode="lines+markers",
                name=team,
                line=dict(color=colors[idx % len(colors)], width=2),
                marker=dict(size=4),
                hovertemplate="Minute: %{x}<br>Pressures: %{y}<extra>" + team + "</extra>",
            )
        )

    fig.update_layout(
        title_text="Pressure Events by Minute",
        xaxis_title="Match Minute",
        yaxis_title="Pressure Events",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color="white"),
        legend=dict(font=dict(color="white"), orientation="h", y=1.08),
        margin=dict(l=40, r=20, t=60, b=50),
        height=320,
    )
    fig.update_xaxes(gridcolor="rgba(255, 255, 255, 0.1)")
    fig.update_yaxes(gridcolor="rgba(255, 255, 255, 0.1)")

    st.plotly_chart(fig, use_container_width=True, key="match_momentum_pressure_timeline_plotly")
