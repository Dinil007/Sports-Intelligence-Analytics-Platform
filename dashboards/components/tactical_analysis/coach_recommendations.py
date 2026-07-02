"""
dashboards/components/tactical_analysis/coach_recommendations.py
===============================================================
Renders coaching recommendations section.
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from services.tactical_analysis_service import generate_coach_recommendations


def render_coach_recommendations(match_dashboard: dict[str, Any]) -> None:
    """Render coaching recommendations as bullet points."""
    st.subheader("Coach Recommendations")
    recommendations = generate_coach_recommendations(match_dashboard)
    if not recommendations:
        st.info("Coaching recommendations are not available.")
        return

    # Handle dict-based recommendations (team-name keys mapped to list)
    if isinstance(recommendations, dict):
        for team_name, team_recs in recommendations.items():
            st.markdown("### " + str(team_name))
            for r in (team_recs or []):
                st.markdown(chr(8226) + " " + str(r))
        return

    # Fallback: plain list of recommendations
    for r in recommendations:
        st.markdown(chr(8226) + " " + str(r))
