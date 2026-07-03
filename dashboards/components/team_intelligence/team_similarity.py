"""Team similarity renderer."""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
import streamlit as st

from services.team_intelligence_service import calculate_team_similarity


def render_team_similarity(events: list[dict[str, Any]]) -> None:
    """Render radar and grouped bar team comparison."""
    st.markdown("### Team Similarity")
    data = calculate_team_similarity(events)
    metrics = data.get("metrics", [])
    normalized = data.get("normalized", {})
    raw = data.get("raw", {})
    if not normalized:
        st.info("No team similarity data available.")
        return

    radar = go.Figure()
    closed_metrics = metrics + metrics[:1]
    for team, values in normalized.items():
        radar.add_trace(go.Scatterpolar(r=[values.get(metric, 0.0) for metric in closed_metrics], theta=closed_metrics, fill="toself", name=team))
    radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), height=430)
    st.plotly_chart(radar, use_container_width=True)

    bars = go.Figure()
    for team, values in raw.items():
        bars.add_bar(name=team, x=metrics, y=[values.get(metric, 0.0) for metric in metrics])
    bars.update_layout(barmode="group", yaxis_title="Raw value", height=390)
    st.plotly_chart(bars, use_container_width=True)
