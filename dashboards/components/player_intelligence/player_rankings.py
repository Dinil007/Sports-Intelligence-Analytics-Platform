"""Top player rankings component."""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from services.player_intelligence_service import calculate_player_rankings


def render_player_rankings(events: list[dict[str, Any]]) -> None:
    """Render top player rankings as a Plotly table."""
    st.subheader("Top Player Rankings")
    if not events:
        st.info("No event data available for player rankings.")
        return

    rankings = calculate_player_rankings(events)[:15]
    if not rankings:
        st.info("No player ranking data calculated.")
        return

    columns = ["Player", "Team", "Score", "Passes", "Shots", "Carries", "Recoveries"]
    values = [
        [row["player"] for row in rankings],
        [row["team"] for row in rankings],
        [row["score"] for row in rankings],
        [row["passes"] for row in rankings],
        [row["shots"] for row in rankings],
        [row["carries"] for row in rankings],
        [row["recoveries"] for row in rankings],
    ]

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(values=columns, fill_color="#0f172a", font=dict(color="white", size=13), align="left"),
                cells=dict(values=values, fill_color="rgba(15, 23, 42, 0.45)", font=dict(color="white", size=12), align="left"),
            )
        ]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=420,
    )
    st.plotly_chart(fig, use_container_width=True, key="player_intelligence_rankings_plotly")
