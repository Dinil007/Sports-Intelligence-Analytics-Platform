"""
dashboards/components/match_intelligence/match_header.py
==========================================================
Match header showing home/away teams, score, and match metadata.
Pure Streamlit. No charts. No HTML. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import streamlit as st


def render_match_header(data: dict[str, Any]) -> None:
    """Render the match header.

    Parameters
    ----------
    data : dict
        The dashboard data dict returned by ``get_match_dashboard()``.
        Expected keys: ``match_info``, ``home_team``, ``away_team``, ``score``.
    """
    match = data.get("match_info") or {}
    home_team = match.get("home_team", data.get("home_team", "Home"))
    away_team = match.get("away_team", data.get("away_team", "Away"))
    score = data.get("score", {})
    home_score = score.get("home", "–")
    away_score = score.get("away", "–")

    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        st.subheader(home_team)
    with col2:
        st.title(f"{home_score} – {away_score}")
    with col3:
        st.subheader(away_team)

    meta_cols = st.columns(5)
    with meta_cols[0]:
        st.caption(f"**Competition:** {match.get('competition_name', '–')}")
    with meta_cols[1]:
        st.caption(f"**Season:** {match.get('season_name', '–')}")
    with meta_cols[2]:
        st.caption(f"**Date:** {match.get('match_date', '–')}")
    with meta_cols[3]:
        st.caption(f"**Kickoff:** {match.get('kick_off', '–')}")
    with meta_cols[4]:
        st.caption("**Venue:** Neutral (venue not available)")
