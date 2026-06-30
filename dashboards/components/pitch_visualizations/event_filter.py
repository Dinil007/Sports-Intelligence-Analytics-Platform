"""
dashboards/components/pitch_visualizations/event_filter.py
============================================================
Event type selector for pitch visualizations.

Returns the selected event type string.
Does NOT write to session_state.
"""

from __future__ import annotations

import streamlit as st

_EVENT_OPTIONS = [
    "All",
    "Pass",
    "Carry",
    "Shot",
    "Pressure",
    "Recovery",
    "Tackle",
    "Interception",
    "Block",
    "Clearance",
]


def render_event_filter() -> str:
    """Render a select box for filtering event types.

    Returns
    -------
    str
        The selected event type, or "All".
    """
    selected = st.selectbox(
        "Event Filter",
        _EVENT_OPTIONS,
        index=0,
        key="match_pitch_event_filter",
    )
    return selected
