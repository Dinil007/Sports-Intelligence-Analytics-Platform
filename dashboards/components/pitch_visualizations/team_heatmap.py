"""
dashboards/components/pitch_visualizations/team_heatmap.py
===========================================================
Overlay touch locations for every player of the selected team.

Plotly only. No HTML. No CSS. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
import streamlit as st

from dashboards.components.pitch_visualizations.football_pitch import render_pitch


def render_team_heatmap(events: list[dict[str, Any]]) -> None:
    """Render a heatmap of touch locations for all players of one team.

    Parameters
    ----------
    events : list[dict]
        Event list from ``match_dashboard["events"]``.
    """
    if not events:
        st.info("No events available for team heatmap.")
        return

    teams = sorted({e.get("team_name") for e in events if e.get("team_name")})
    if not teams:
        st.info("No team data available.")
        return

    selected_team = st.selectbox(
        "Select Team",
        teams,
        key="match_team_heatmap_team",
    )

    team_events = [
        e for e in events
        if e.get("team_name") == selected_team
        and e.get("location") is not None
    ]

    if not team_events:
        st.info(
            f"Pitch coordinates are unavailable for {selected_team}."
        )
        return

    fig = render_pitch()

    x_coords = [e["location"][0] for e in team_events]
    y_coords = [e["location"][1] for e in team_events]

    fig.add_trace(
        go.Scatter(
            x=x_coords,
            y=y_coords,
            mode="markers",
            marker=dict(
                size=6,
                color=list(range(len(team_events))),
                colorscale="YlOrRd",
                opacity=0.7,
                colorbar=dict(title="Event Count"),
            ),
            hovertemplate=(
                "Minute: %{customdata[0]}<br>"
                "Event: %{customdata[1]}<br>"
                "Player: %{customdata[2]}<extra></extra>"
            ),
            customdata=[
                [
                    e.get("minute"),
                    e.get("event_type"),
                    e.get("player_name"),
                ]
                for e in team_events
            ],
            name=selected_team,
        )
    )

    fig.update_layout(
        title=f"Team Touch Heatmap — {selected_team}",
        width=900,
        height=500,
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    st.plotly_chart(fig, use_container_width=True, key="match_team_heatmap")
