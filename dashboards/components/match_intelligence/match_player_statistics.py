"""
dashboards/components/match_intelligence/match_player_statistics.py
=====================================================================
Player statistics table for Match Intelligence.

Uses ``st.dataframe``.
No charts. No HTML. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import streamlit as st


def render_match_player_statistics(data: dict[str, Any]) -> None:
    """Render per-player statistics.

    Columns: Player, Team, Goals, Passes, Recoveries, Pressures, Minutes

    Parameters
    ----------
    data : dict
        Dashboard data from ``get_match_dashboard()``.
        Expected key: ``player_statistics`` — list of dicts.
    """
    players = data.get("player_statistics", [])
    if not players:
        st.info("No player statistics available.")
        return

    df = []
    for p in players:
        df.append({
            "Player": p.get("player_name", "Unknown"),
            "Team": p.get("team_name"),
            "Goals": p.get("goals", 0),
            "Passes": p.get("passes", 0),
            "Recoveries": p.get("recoveries", 0),
            "Pressures": p.get("pressures", 0),
            "Minutes": p.get("minutes_played", 0),
        })

    st.dataframe(df, use_container_width=True, hide_index=True)
