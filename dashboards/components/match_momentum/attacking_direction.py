"""Attacking direction chart."""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from services.match_momentum_service import calculate_attacking_direction


def render_attacking_direction(events: list[dict[str, Any]]) -> None:
    """Render final-third attacking activity by lane."""
    st.subheader("Attacking Direction")
    if not events:
        st.info("No event data available for attacking direction.")
        return

    directions = calculate_attacking_direction(events)
    if not directions:
        st.info("No attacking direction data calculated.")
        return

    lanes = ["Left Wing", "Half Space Left", "Central", "Half Space Right", "Right Wing"]
    fig = go.Figure()
    colors = ["#10b981", "#3b82f6", "#eab308", "#a855f7"]
    for idx, (team, lane_counts) in enumerate(directions.items()):
        values = [lane_counts.get(lane, 0) for lane in lanes]
        fig.add_trace(
            go.Bar(
                y=lanes,
                x=values,
                name=team,
                orientation="h",
                marker=dict(color=colors[idx % len(colors)], line=dict(color="white", width=1)),
                text=values,
                textposition="auto",
                hovertemplate="Lane: %{y}<br>Actions: %{x}<extra>" + team + "</extra>",
            )
        )

    fig.update_layout(
        title_text="Attacking Activity by Lane",
        xaxis_title="Attacking Actions",
        barmode="group",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color="white"),
        legend=dict(font=dict(color="white"), orientation="h", y=1.08),
        margin=dict(l=150, r=20, t=60, b=50),
        height=360,
    )
    fig.update_xaxes(gridcolor="rgba(255, 255, 255, 0.1)")

    st.plotly_chart(fig, use_container_width=True, key="match_momentum_attacking_direction_plotly")
