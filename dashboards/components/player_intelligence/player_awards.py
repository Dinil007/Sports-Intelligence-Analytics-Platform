"""Player awards component."""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from services.player_intelligence_service import generate_player_awards


def render_player_awards(events: list[dict[str, Any]]) -> None:
    """Render deterministic match awards."""
    st.subheader("Match Awards")
    if not events:
        st.info("No event data available for player awards.")
        return

    awards = generate_player_awards(events)
    if not awards:
        st.info("No player awards generated.")
        return

    award_names = list(awards.keys())
    rows = [awards[name] for name in award_names]
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(values=["Award", "Player", "Team", "Metric", "Value"], fill_color="#0f172a", font=dict(color="white", size=13), align="left"),
                cells=dict(
                    values=[
                        award_names,
                        [row["player"] for row in rows],
                        [row["team"] for row in rows],
                        [row["metric"] for row in rows],
                        [row["value"] for row in rows],
                    ],
                    fill_color="rgba(15, 23, 42, 0.45)",
                    font=dict(color="white", size=12),
                    align="left",
                ),
            )
        ]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=280,
    )
    st.plotly_chart(fig, use_container_width=True, key="player_intelligence_awards_plotly")
