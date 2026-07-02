"""
dashboards/components/tactical_analysis/tactical_dashboard.py
=============================================================
Orchestrator for all tactical analysis UI components.

Calls existing tactical analysis UI components for all five sections.
No calculations. No SQL. No business logic.
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from dashboards.components.tactical_analysis.coach_recommendations import (
    render_coach_recommendations,
)
from dashboards.components.tactical_analysis.match_verdict import render_match_verdict
from dashboards.components.tactical_analysis.tactical_summary import (
    render_tactical_summary,
)
from dashboards.components.tactical_analysis.team_strengths import render_team_strengths
from dashboards.components.tactical_analysis.team_weaknesses import render_team_weaknesses


def render_tactical_dashboard(match_dashboard: dict[str, Any]) -> None:
    """Render the complete tactical analysis dashboard.

    Parameters
    ----------
    match_dashboard : dict
        The full dashboard dict returned by ``get_match_dashboard()``.
    """
    if not match_dashboard:
        st.info("No match data available for tactical analysis.")
        return

    st.header("AI Tactical Analysis")

    # Executive Summary
    with st.container():
        render_tactical_summary(match_dashboard)

    st.divider()

    # Strengths & Weaknesses in a 2-column layout
    col1, col2 = st.columns(2)

    with col1:
        render_team_strengths(match_dashboard)

    with col2:
        render_team_weaknesses(match_dashboard)

    st.divider()

    # Coach Recommendations
    with st.container():
        render_coach_recommendations(match_dashboard)

    st.divider()

    # Final Verdict
    with st.container():
        render_match_verdict(match_dashboard)
