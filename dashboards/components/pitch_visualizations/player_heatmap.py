"""
dashboards/components/pitch_visualizations/player_heatmap.py
=============================================================
Overlay touch locations for a selected player on the football pitch.

Plotly only. No HTML. No CSS. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
import streamlit as st

from dashboards.components.pitch_visualizations.football_pitch import render_pitch


def render_player_heatmap(events: list[dict[str, Any]]) -> None:
    """Render a heatmap of touch locations for one player.

    Parameters
    ----------
    events : list[dict]
        Event list from ``match_dashboard["events"]``.
    """
    if not events:
        st.info("No events available for heatmap.")
        return

    players = sorted(
        {e.get("player_name") for e in events if e.get("player_name")}
    )
    if not players:
        st.info("No player data available.")
        return

    selected_player = st.selectbox(
        "Select Player",
        players,
        key="match_player_heatmap_player",
    )

    player_events = [
        e for e in events
        if e.get("player_name") == selected_player
        and e.get("location") is not None
    ]

    if not player_events:
        st.info(
            "Pitch coordinates are unavailable for this player's events."
        )
        return

    fig = render_pitch()

    x_coords = [e["location"][0] for e in player_events]
    y_coords = [e["location"][1] for e in player_events]

    fig.add_trace(
        go.Scatter(
            x=x_coords,
            y=y_coords,
            mode="markers",
            marker=dict(
                size=8,
                color=list(range(len(player_events))),
                colorscale="YlOrRd",
                opacity=0.8,
                colorbar=dict(title="Event Count"),
            ),
            hovertemplate=(
                "Minute: %{customdata[0]}<br>"
                "Event: %{customdata[1]}<br>"
                "Player: %{customdata[2]}<extra></extra>"
            ),
            customdata=[
                [e.get("minute"), e.get("event_type"), selected_player]
                for e in player_events
            ],
            name=selected_player,
        )
    )

    fig.update_layout(
        title=f"Touch Heatmap — {selected_player}",
        width=900,
        height=500,
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    st.plotly_chart(fig, use_container_width=True, key="match_player_heatmap")
