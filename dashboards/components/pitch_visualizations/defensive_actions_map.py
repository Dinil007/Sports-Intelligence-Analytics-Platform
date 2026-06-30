"""
dashboards/components/pitch_visualizations/defensive_actions_map.py
===================================================================
Display defensive actions with distinct marker colors.

Covers: Tackles, Interceptions, Blocks, Clearances, Recoveries.

Plotly only. No HTML. No CSS. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
import streamlit as st

from dashboards.components.pitch_visualizations.football_pitch import render_pitch

_DEFENSIVE_EVENT_TYPES = {
    "Tackle",
    "Interception",
    "Block",
    "Clearance",
    "Ball Recovery",
}

_DEFENSIVE_COLORS = {
    "Tackle": "#ef4444",
    "Interception": "#f59e0b",
    "Block": "#8b5cf6",
    "Clearance": "#06b6d4",
    "Ball Recovery": "#22c55e",
}

_DEFENSIVE_SYMBOLS = {
    "Tackle": "circle",
    "Interception": "diamond",
    "Block": "square",
    "Clearance": "triangle-up",
    "Ball Recovery": "star",
}


def render_defensive_actions(events: list[dict[str, Any]]) -> None:
    """Render defensive action locations on the football pitch.

    Parameters
    ----------
    events : list[dict]
        Event list from ``match_dashboard["events"]``.
    """
    if not events:
        st.info("No events available for defensive actions map.")
        return

    defensive_events = [
        e for e in events
        if e.get("event_type") in _DEFENSIVE_EVENT_TYPES
        and e.get("location") is not None
    ]

    if not defensive_events:
        st.info("Pitch coordinates are unavailable for this event type.")
        return

    fig = render_pitch()

    # Group defensive events by type for efficient rendering.
    events_by_type: dict[str, list[dict[str, Any]]] = {}
    for e in defensive_events:
        event_type = e.get("event_type", "Unknown")
        events_by_type.setdefault(event_type, []).append(e)

    # Render each event type as a single trace.
    for event_type, events in events_by_type.items():
        color = _DEFENSIVE_COLORS.get(event_type, "#6b7280")
        symbol = _DEFENSIVE_SYMBOLS.get(event_type, "circle")

        x_coords = [e["location"][0] for e in events]
        y_coords = [e["location"][1] for e in events]

        fig.add_trace(
            go.Scatter(
                x=x_coords,
                y=y_coords,
                mode="markers",
                marker=dict(
                    size=9,
                    color=color,
                    symbol=symbol,
                    line=dict(width=1, color="white"),
                    opacity=0.85,
                ),
                name=event_type,
                hovertemplate=(
                    "Type: %{customdata[0]}<br>"
                    "Player: %{customdata[1]}<br>"
                    "Minute: %{customdata[2]}<extra></extra>"
                ),
                customdata=[
                    [
                        event_type,
                        e.get("player_name"),
                        e.get("minute"),
                    ]
                    for e in events
                ],
                showlegend=True,
            )
        )

    fig.update_layout(
        title="Defensive Actions",
        width=900,
        height=500,
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    st.plotly_chart(fig, use_container_width=True, key="match_defensive_actions_map")
