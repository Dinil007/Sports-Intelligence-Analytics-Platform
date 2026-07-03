"""Playing style renderer."""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
import streamlit as st

from services.team_intelligence_service import detect_playing_style


def render_playing_style(events: list[dict[str, Any]]) -> None:
    """Render deterministic team playing styles."""
    st.markdown("### Playing Style")
    styles = detect_playing_style(events)
    if not styles:
        st.info("No playing style data available.")
        return

    fig = go.Figure(
        data=[
            go.Bar(
                x=list(styles),
                y=[1 for _ in styles],
                text=list(styles.values()),
                textposition="inside",
                hovertext=[f"{team}: {style}" for team, style in styles.items()],
                hoverinfo="text",
            )
        ]
    )
    fig.update_layout(yaxis=dict(visible=False), xaxis_title="", showlegend=False, height=260)
    st.plotly_chart(fig, use_container_width=True)
