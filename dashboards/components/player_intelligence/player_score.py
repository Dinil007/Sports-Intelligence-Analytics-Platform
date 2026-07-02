"""Player performance score component."""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from services.player_intelligence_service import calculate_player_scores


def render_player_scores(events: list[dict[str, Any]]) -> None:
    """Render deterministic player performance score."""
    st.subheader("Player Performance Score")
    if not events:
        st.info("No event data available for player scores.")
        return

    scores = calculate_player_scores(events)
    if not scores:
        st.info("No player score data calculated.")
        return

    players = sorted(scores.keys(), key=lambda player: scores[player]["score"], reverse=True)
    selected_player = st.selectbox("Select Player for Performance Score", players, key="player_intel_score_select")
    row = scores[selected_player]
    stars = chr(9733) * int(row.get("stars", 0)) + chr(9734) * (5 - int(row.get("stars", 0)))

    fig = go.Figure()
    fig.add_trace(
        go.Indicator(
            mode="number+gauge",
            value=float(row.get("score", 0.0)),
            number=dict(font=dict(color="#10b981", size=44), suffix=" / 10"),
            title=dict(text=f"{selected_player}<br>{stars}", font=dict(color="white", size=16)),
            gauge=dict(
                axis=dict(range=[0, 10], tickfont=dict(color="white")),
                bar=dict(color="#10b981"),
                bgcolor="rgba(15, 23, 42, 0.6)",
                bordercolor="rgba(255, 255, 255, 0.2)",
            ),
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=20, r=20, t=40, b=20),
        height=260,
    )
    st.plotly_chart(fig, use_container_width=True, key="player_intelligence_score_plotly")
