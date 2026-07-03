"""Zone dominance renderer."""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
import streamlit as st

from services.team_intelligence_service import calculate_zone_dominance


def render_zone_dominance(events: list[dict[str, Any]]) -> None:
    """Render pitch lane and third dominance percentages."""
    st.markdown("### Zone Dominance")
    data = calculate_zone_dominance(events)
    if not data:
        st.info("No zone dominance data available.")
        return

    teams = list(data)
    zones = [
        "Left Wing",
        "Left Half Space",
        "Centre",
        "Right Half Space",
        "Right Wing",
        "Defensive Third",
        "Middle Third",
        "Attacking Third",
    ]
    fig = go.Figure()
    for team in teams:
        fig.add_bar(name=team, x=zones, y=[data[team].get(zone, 0.0) for zone in zones])
    fig.update_layout(barmode="group", yaxis_title="Action share (%)", height=420)
    st.plotly_chart(fig, use_container_width=True)
