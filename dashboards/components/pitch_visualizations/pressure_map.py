"""
dashboards/components/pitch_visualizations/pressure_map.py
===========================================================
Display pressure event locations.

Plotly only. No HTML. No CSS. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
import streamlit as st

from dashboards.components.pitch_visualizations.football_pitch import render_pitch


def render_pressure_map(events: list[dict[str, Any]]) -> None:
    """Render pressure event locations on the football pitch.

    Parameters
    ----------
    events : list[dict]
        Event list from ``match_dashboard["events"]``.
    """
    if not events:
        st.info("No events available for pressure map.")
        return

    pressure_events = [
        e for e in events
        if e.get("event_type") == "Pressure"
        and e.get("location") is not None
    ]

    if not pressure_events:
        st.info("Pitch coordinates are unavailable for this event type.")
        return

    fig = render_pitch()

    x_coords = [e["location"][0] for e in pressure_events]
    y_coords = [e["location"][1] for e in pressure_events]

    fig.add_trace(
        go.Scatter(
            x=x_coords,
            y=y_coords,
            mode="markers",
            marker=dict(
                size=10,
                color="#f97316",
                symbol="triangle-up",
                line=dict(width=1, color="white"),
                opacity=0.8,
            ),
            hovertemplate=(
                "Minute: %{customdata[0]}<br>"
                "Player: %{customdata[1]}<br>"
                "Team: %{customdata[2]}<extra></extra>"
            ),
            customdata=[
                [
                    e.get("minute"),
                    e.get("player_name"),
                    e.get("team_name"),
                ]
                for e in pressure_events
            ],
            name="Pressure",
        )
    )

    fig.update_layout(
        title="Pressure Map",
        width=900,
        height=500,
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    st.plotly_chart(fig, use_container_width=True, key="match_pressure_map")
