"""Build-up play renderer."""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
import streamlit as st

from services.team_intelligence_service import calculate_build_up_play


def render_build_up_play(events: list[dict[str, Any]]) -> None:
    """Render build-up play characteristics."""
    st.markdown("### Build-up Play")
    data = calculate_build_up_play(events)
    if not data:
        st.info("No build-up play data available.")
        return

    teams = list(data)
    categories = ["Short Build-up", "Direct Build-up", "Progressive Build-up", "Wide Build-up", "Central Build-up"]
    fig = go.Figure()
    for category in categories:
        fig.add_bar(name=category, x=teams, y=[data[team].get(category, 0.0) for team in teams])
    fig.update_layout(barmode="stack", yaxis_title="Share of actions (%)", height=390)
    st.plotly_chart(fig, use_container_width=True)
