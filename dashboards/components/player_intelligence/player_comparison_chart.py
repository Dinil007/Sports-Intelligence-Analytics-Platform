"""Player comparison chart."""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from services.player_intelligence_service import calculate_player_statistics


def render_player_comparison(events: list[dict[str, Any]]) -> None:
    """Render grouped bars comparing two players."""
    st.subheader("Player Comparison")
    if not events:
        st.info("No event data available for player comparison.")
        return

    stats = calculate_player_statistics(events)
    players = sorted(stats.keys())
    if len(players) < 2:
        st.info("At least two players are required for comparison.")
        return

    player_a = st.selectbox("Select Player A", players, key="player_intel_compare_a")
    player_b_options = [player for player in players if player != player_a]
    player_b = st.selectbox("Select Player B", player_b_options, key="player_intel_compare_b")
    metrics = ["passes", "shots", "carries", "pressures", "recoveries", "tackles"]
    labels = [metric.title() for metric in metrics]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=labels,
            y=[stats[player_a].get(metric, 0) for metric in metrics],
            name=player_a,
            marker=dict(color="#10b981", line=dict(color="white", width=1)),
        )
    )
    fig.add_trace(
        go.Bar(
            x=labels,
            y=[stats[player_b].get(metric, 0) for metric in metrics],
            name=player_b,
            marker=dict(color="#3b82f6", line=dict(color="white", width=1)),
        )
    )
    fig.update_layout(
        title_text="Player A vs Player B",
        xaxis_title="Metric",
        yaxis_title="Count",
        barmode="group",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color="white"),
        legend=dict(font=dict(color="white"), orientation="h", y=1.08),
        margin=dict(l=40, r=20, t=60, b=50),
        height=340,
    )
    fig.update_yaxes(gridcolor="rgba(255, 255, 255, 0.1)")
    st.plotly_chart(fig, use_container_width=True, key="player_intelligence_comparison_plotly")
