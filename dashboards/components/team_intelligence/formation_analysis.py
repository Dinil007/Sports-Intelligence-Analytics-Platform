"""Formation analysis renderer."""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
import streamlit as st

from services.team_intelligence_service import detect_team_formation


def render_formation_analysis(events: list[dict[str, Any]]) -> None:
    """Render deterministic formation analysis."""
    st.markdown("### Formation Analysis")
    formations = detect_team_formation(events)
    if not formations:
        st.info("No formation data available.")
        return

    teams = list(formations)
    fig = go.Figure(
        data=[
            go.Bar(
                x=teams,
                y=[1 for _ in teams],
                text=[formations[team] for team in teams],
                textposition="inside",
                hovertext=[f"{team}: {formations[team]}" for team in teams],
                hoverinfo="text",
            )
        ]
    )
    fig.update_layout(yaxis=dict(visible=False), xaxis_title="", showlegend=False, height=260)
    st.plotly_chart(fig, use_container_width=True)
