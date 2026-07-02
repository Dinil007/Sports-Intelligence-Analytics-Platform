"""
dashboards/components/tactical_analysis/team_weaknesses.py
============================================================
Renders team weaknesses section.
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from services.tactical_analysis_service import generate_team_weaknesses


def render_team_weaknesses(match_dashboard: dict[str, Any]) -> None:
    """Render team weaknesses as bullet points."""
    st.subheader("Weaknesses")
    weaknesses = generate_team_weaknesses(match_dashboard)
    if not weaknesses:
        st.info("Weaknesses analysis is not available.")
        return

    # Handle dict-based weaknesses (team-name keys mapped to list of weaknesses)
    if isinstance(weaknesses, dict):
        for team_name, team_weaknesses in weaknesses.items():
            st.markdown("### " + str(team_name))
            for w in (team_weaknesses or []):
                st.markdown(chr(10007) + " " + str(w))
        return

    # Fallback: plain list of weaknesses (render as cross-marked bullets)
    for w in weaknesses:
        st.markdown(chr(10007) + " " + str(w))
