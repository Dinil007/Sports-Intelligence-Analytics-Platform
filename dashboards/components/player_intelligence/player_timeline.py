"""Player event timeline."""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from services.player_intelligence_service import calculate_player_timeline


def render_player_timeline(events: list[dict[str, Any]]) -> None:
    """Render cumulative player events by minute."""
    st.subheader("Player Timeline")
    if not events:
        st.info("No event data available for player timeline.")
        return

    timeline = calculate_player_timeline(events)
    minutes = timeline.get("minutes", [])
    players = timeline.get("players", {})
    if not minutes or not players:
        st.info("No player timeline data calculated.")
        return

    selected_player = st.selectbox("Select Player for Timeline", sorted(players.keys()), key="player_intel_timeline_player")
    metric = st.selectbox("Select Timeline Metric", ["Passes", "Carries", "Pressures", "Recoveries"], key="player_intel_timeline_metric")
    values = players.get(selected_player, {}).get(metric, [])

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=minutes,
            y=values,
            mode="lines",
            name=f"{selected_player} - {metric}",
            line=dict(color="#3b82f6", width=3),
            hovertemplate="Minute: %{x}<br>Cumulative " + metric + ": %{y}<extra></extra>",
        )
    )
    fig.update_layout(
        title_text=f"Cumulative {metric}: {selected_player}",
        xaxis_title="Match Minute",
        yaxis_title=metric,
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color="white"),
        margin=dict(l=40, r=20, t=60, b=50),
        height=340,
    )
    fig.update_xaxes(gridcolor="rgba(255, 255, 255, 0.1)")
    fig.update_yaxes(gridcolor="rgba(255, 255, 255, 0.1)")

    st.plotly_chart(fig, use_container_width=True, key="player_intelligence_timeline_plotly")
