"""
dashboards/components/tactical_analysis/team_strengths.py
============================================================
Renders team strengths section.
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from services.tactical_analysis_service import generate_team_strengths


def render_team_strengths(match_dashboard: dict[str, Any]) -> None:
    """Render team strengths as bullet points."""
    st.subheader("Strengths")
    strengths = generate_team_strengths(match_dashboard)
    if not strengths:
        st.info("Strengths analysis is not available.")
        return

    # Handle dict-based strengths (team-name keys mapped to list of strengths)
    if isinstance(strengths, dict):
        for team_name, team_strengths in strengths.items():
            st.markdown("### " + str(team_name))
            for s in (team_strengths or []):
                st.markdown(chr(10003) + " " + str(s))
        return

    # Fallback: plain list of strengths (render as checkmarked bullets)
    for s in strengths:
        st.markdown(chr(10003) + " " + str(s))
