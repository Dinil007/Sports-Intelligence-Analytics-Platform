"""Player role detection component."""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from services.player_intelligence_service import detect_player_roles


def render_player_roles(events: list[dict[str, Any]]) -> None:
    """Render deterministic player role detection results."""
    st.subheader("Detected Player Roles")
    if not events:
        st.info("No event data available for player roles.")
        return

    roles = detect_player_roles(events)
    if not roles:
        st.info("No player roles detected.")
        return

    rows = list(roles.values())[:20]
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(values=["Player", "Team", "Detected Role"], fill_color="#0f172a", font=dict(color="white", size=13), align="left"),
                cells=dict(
                    values=[[row["player"] for row in rows], [row["team"] for row in rows], [row["role"] for row in rows]],
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
        height=420,
    )
    st.plotly_chart(fig, use_container_width=True, key="player_intelligence_roles_plotly")
