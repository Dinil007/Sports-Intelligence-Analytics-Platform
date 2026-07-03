"""Expected threat renderer."""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
import streamlit as st

from services.team_intelligence_service import calculate_expected_threat


def render_expected_threat(events: list[dict[str, Any]]) -> None:
    """Render deterministic expected threat outputs."""
    st.markdown("### Expected Threat (xT)")
    data = calculate_expected_threat(events)
    teams = data.get("teams", [])
    players = data.get("players", [])
    actions = data.get("actions", [])
    if not teams and not players and not actions:
        st.info("No expected threat data available.")
        return

    if teams:
        fig = go.Figure(data=[go.Bar(x=[item["team"] for item in teams], y=[item["xT"] for item in teams], name="Team xT")])
        fig.update_layout(yaxis_title="xT", height=310)
        st.plotly_chart(fig, use_container_width=True)
    if players:
        fig_players = go.Figure(data=[go.Bar(x=[item["player"] for item in players], y=[item["xT"] for item in players], name="Player xT")])
        fig_players.update_layout(yaxis_title="xT", height=360)
        st.plotly_chart(fig_players, use_container_width=True)
    if actions:
        st.dataframe(actions, use_container_width=True)
