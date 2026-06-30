"""
dashboards/components/match_intelligence/match_timeline.py
===========================================================
Match timeline table for Match Intelligence.

Uses ``st.dataframe``.
No charts. No HTML. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import streamlit as st


def render_match_timeline(data: dict[str, Any]) -> None:
    """Render the match timeline as a dataframe.

    Columns: Minute, Team, Player, Event, Outcome.

    Parameters
    ----------
    data : dict
        Dashboard data from ``get_match_dashboard()``.
        Expected key: ``timeline`` — list of dicts.
    """
    timeline = data.get("timeline", [])
    if not timeline:
        st.info("No timeline events available.")
        return

    df = []
    for e in timeline:
        df.append({
            "Minute": e.get("minute"),
            "Team": e.get("team_name"),
            "Player": e.get("player_name"),
            "Event": e.get("event_type"),
            "Outcome": e.get("play_pattern"),
        })

    st.dataframe(df, use_container_width=True, hide_index=True)
