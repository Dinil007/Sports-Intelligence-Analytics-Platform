"""Player influence map."""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from dashboards.components.pitch_visualizations.football_pitch import render_pitch
from services.player_intelligence_service import calculate_player_influence


def render_player_influence(events: list[dict[str, Any]]) -> None:
    """Render player touch locations on the existing Plotly football pitch."""
    st.subheader("Player Influence Map")
    if not events:
        st.info("No event data available for player influence map.")
        return

    influence = calculate_player_influence(events)
    if not influence:
        st.info("No player influence data calculated.")
        return

    players = sorted(influence.keys())
    selected_player = st.selectbox("Select Player for Influence Map", players, key="player_intel_influence_select")
    touches = influence.get(selected_player, [])
    if not touches:
        st.info("No touch locations available for selected player.")
        return

    fig = render_pitch()
    fig.add_trace(
        go.Scatter(
            x=[touch["x"] for touch in touches],
            y=[touch["y"] for touch in touches],
            mode="markers",
            name=selected_player,
            marker=dict(size=8, color="#10b981", opacity=0.72, line=dict(color="white", width=1)),
            text=[touch["event_type"] for touch in touches],
            customdata=[touch["minute"] for touch in touches],
            hovertemplate="%{text}<br>Minute: %{customdata}<br>x=%{x}, y=%{y}<extra>" + selected_player + "</extra>",
        )
    )
    fig.update_layout(
        title=dict(text=f"Touch Map: {selected_player}", font=dict(color="white", size=16), x=0.5, xanchor="center"),
        height=520,
    )

    st.plotly_chart(fig, use_container_width=True, key="player_intelligence_influence_plotly")
