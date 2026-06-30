"""
dashboards/components/match_intelligence/match_events.py
==========================================================
Raw events table for Match Intelligence.

Uses ``st.dataframe``.
No processing. No charts. No HTML. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import streamlit as st


def render_match_events(data: dict[str, Any]) -> None:
    """Render raw match events.

    Parameters
    ----------
    data : dict
        Dashboard data from ``get_match_dashboard()``.
        Expected key: ``events`` — list of event dicts.
    """
    events = data.get("events", [])
    if not events:
        st.info("No events available.")
        return

    st.dataframe(events, use_container_width=True, hide_index=True)
