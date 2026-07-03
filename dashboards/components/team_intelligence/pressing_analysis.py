"""Pressing analysis renderer."""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
import streamlit as st

from services.team_intelligence_service import calculate_pressing_analysis


def render_pressing_analysis(events: list[dict[str, Any]]) -> None:
    """Render pressing zones, pressure timeline, and success."""
    st.markdown("### Pressing Analysis")
    data = calculate_pressing_analysis(events)
    zones = data.get("zones", {})
    if not zones:
        st.info("No pressing data available.")
        return

    teams = list(zones)
    fig = go.Figure()
    for zone in ["High Press", "Mid Block", "Low Block"]:
        fig.add_bar(name=zone, x=teams, y=[zones[team].get(zone, 0) for team in teams])
    fig.update_layout(barmode="group", yaxis_title="Pressures", height=350)
    st.plotly_chart(fig, use_container_width=True)

    timeline = data.get("timeline", {})
    fig_timeline = go.Figure()
    for team, values in timeline.items():
        fig_timeline.add_trace(go.Scatter(x=data.get("minutes", []), y=values, mode="lines", name=team))
    fig_timeline.update_layout(xaxis_title="Minute", yaxis_title="Pressures", height=330)
    st.plotly_chart(fig_timeline, use_container_width=True)

    success = data.get("success", {})
    st.dataframe([{"Team": team, "Pressure Success": f"{value}%"} for team, value in success.items()], use_container_width=True)
