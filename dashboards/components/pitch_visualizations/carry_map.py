"""
dashboards/components/pitch_visualizations/carry_map.py
========================================================
Display player carries with start and end locations.

Plotly only. No HTML. No CSS. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
import streamlit as st

from dashboards.components.pitch_visualizations.football_pitch import render_pitch


def render_carry_map(events: list[dict[str, Any]]) -> None:
    """Render carry events on the football pitch.

    Parameters
    ----------
    events : list[dict]
        Event list from ``match_dashboard["events"]``.
    """
    if not events:
        st.info("No events available for carry map.")
        return

    carry_events = [
        e for e in events
        if e.get("event_type") == "Carry"
        and e.get("location") is not None
        and e.get("carry_end_location") is not None
    ]

    if not carry_events:
        st.info("Pitch coordinates are unavailable for this event type.")
        return

    fig = render_pitch()

    start_x = [e["location"][0] for e in carry_events]
    start_y = [e["location"][1] for e in carry_events]

    fig.add_trace(
        go.Scatter(
            x=start_x,
            y=start_y,
            mode="markers",
            marker=dict(
                size=8,
                color="#3b82f6",
                line=dict(width=1, color="white"),
            ),
            name="Carry Start",
            hovertemplate=(
                "Start: %{customdata[0]}<br>"
                "End: %{customdata[1]}<br>"
                "Player: %{customdata[2]}<extra></extra>"
            ),
            customdata=[
                [
                    f"({e['location'][0]:.1f}, {e['location'][1]:.1f})",
                    f"({e['carry_end_location'][0]:.1f}, {e['carry_end_location'][1]:.1f})",
                    e.get("player_name"),
                ]
                for e in carry_events
            ],
        )
    )

    end_x = [e["carry_end_location"][0] for e in carry_events]
    end_y = [e["carry_end_location"][1] for e in carry_events]

    fig.add_trace(
        go.Scatter(
            x=end_x,
            y=end_y,
            mode="markers",
            marker=dict(
                size=6,
                color="#22c55e",
                symbol="triangle-up",
                line=dict(width=1, color="white"),
            ),
            name="Carry End",
        )
    )

    # Draw carry lines using a single trace with None separators.
    line_x = []
    line_y = []
    for e in carry_events:
        sx, sy = e["location"]
        ex, ey = e["carry_end_location"]
        line_x.extend([sx, ex, None])
        line_y.extend([sy, ey, None])

    fig.add_trace(
        go.Scatter(
            x=line_x,
            y=line_y,
            mode="lines",
            line=dict(
                color="#22c55e",
                width=1.5,
            ),
            opacity=0.7,
            name="Carry",
            showlegend=False,
        )
    )

    fig.update_layout(
        title="Carry Map",
        width=900,
        height=500,
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    st.plotly_chart(fig, use_container_width=True, key="match_carry_map")
