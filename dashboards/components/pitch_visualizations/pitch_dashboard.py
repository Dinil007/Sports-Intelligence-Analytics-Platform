"""
dashboards/components/pitch_visualizations/pitch_dashboard.py
==============================================================
Orchestrator for pitch visualizations.

Responsibilities:
    - Read events from match_dashboard.
    - Render Event Filter.
    - Render Player Heatmap, Team Heatmap, Shot Map, Pass Map,
      Carry Map, Pressure Map, Defensive Action Map.

No calculations. No SQL. No business logic.
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from dashboards.components.pitch_visualizations.carry_map import (
    render_carry_map,
)
from dashboards.components.pitch_visualizations.defensive_actions_map import (
    render_defensive_actions,
)
from dashboards.components.pitch_visualizations.event_filter import (
    render_event_filter,
)
from dashboards.components.pitch_visualizations.pass_map import (
    render_pass_map,
)
from dashboards.components.pitch_visualizations.player_heatmap import (
    render_player_heatmap,
)
from dashboards.components.pitch_visualizations.pressure_map import (
    render_pressure_map,
)
from dashboards.components.pitch_visualizations.shot_map import (
    render_shot_map,
)
from dashboards.components.pitch_visualizations.team_heatmap import (
    render_team_heatmap,
)


def _filter_events(
    events: list[dict[str, Any]], event_type: str
) -> list[dict[str, Any]]:
    """Filter events based on the selected event type.

    Parameters
    ----------
    events : list[dict]
        Raw event list.
    event_type : str
        Selected event type.

    Returns
    -------
    list[dict]
        Filtered events.
    """
    if event_type == "All":
        return events

    # Special mapping for filter names to event types.
    filter_map = {
        "Recovery": "Ball Recovery",
        "Tackle": "Tackle",
        "Interception": "Interception",
        "Block": "Block",
        "Clearance": "Clearance",
    }

    target_type = filter_map.get(event_type, event_type)
    return [e for e in events if e.get("event_type") == target_type]


def render_pitch_dashboard(match_dashboard: dict[str, Any]) -> None:
    """Render the full pitch visualization dashboard.

    Parameters
    ----------
    match_dashboard : dict
        The full dashboard dict returned by ``get_match_dashboard()``.
    """
    events = match_dashboard.get("events", [])

    if not events:
        st.info("No events available for pitch visualizations.")
        return

    st.subheader("Pitch Visualizations")

    event_type = render_event_filter()
    filtered_events = _filter_events(events, event_type)

    # If a specific type is selected, check if any events have coordinates.
    has_any_coordinates = any(
        e.get("location") is not None or (
            e.get("pass_end_location") is not None
            or e.get("carry_end_location") is not None
            or e.get("shot_end_location") is not None
        )
        for e in filtered_events
    )

    if not has_any_coordinates:
        st.info("Pitch coordinates are unavailable for this event type.")
        return

    with st.container():
        st.subheader("Player Heatmap")
        try:
            render_player_heatmap(filtered_events)
        except Exception:
            st.info("Unable to render player heatmap.")

    st.divider()

    with st.container():
        st.subheader("Team Heatmap")
        try:
            render_team_heatmap(filtered_events)
        except Exception:
            st.info("Unable to render team heatmap.")

    st.divider()

    with st.container():
        st.subheader("Shot Map")
        try:
            render_shot_map(filtered_events)
        except Exception:
            st.info("Unable to render shot map.")

    st.divider()

    with st.container():
        st.subheader("Pass Map")
        try:
            render_pass_map(filtered_events)
        except Exception:
            st.info("Unable to render pass map.")

    st.divider()

    with st.container():
        st.subheader("Carry Map")
        try:
            render_carry_map(filtered_events)
        except Exception:
            st.info("Unable to render carry map.")

    st.divider()

    with st.container():
        st.subheader("Pressure Map")
        try:
            render_pressure_map(filtered_events)
        except Exception:
            st.info("Unable to render pressure map.")

    st.divider()

    with st.container():
        st.subheader("Defensive Actions")
        try:
            render_defensive_actions(filtered_events)
        except Exception:
            st.info("Unable to render defensive actions.")
