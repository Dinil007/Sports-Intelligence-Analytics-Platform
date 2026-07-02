"""
dashboards/components/tactical_analysis/tactical_dashboard.py
=============================================================
Orchestrator for all tactical analysis UI components.

Calls generate_full_tactical_analysis() and renders all five sections.
No calculations. No SQL. No business logic.
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from services.tactical_analysis_service import generate_full_tactical_analysis


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

    analysis = generate_full_tactical_analysis(match_dashboard)

    # Executive Summary
    with st.container():
        st.subheader("Executive Summary")
        summary = analysis.get("summary", "")
        if summary:
            st.markdown(summary)
        else:
            st.info("Tactical summary is not available.")

    st.divider()

    # Strengths & Weaknesses in a 2-column layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Strengths")
        strengths = analysis.get("strengths", [])
        if strengths:
            for s in strengths:
                st.markdown(f"- {s}")
        else:
            st.info("No strengths data available.")

    with col2:
        st.subheader("Weaknesses")
        weaknesses = analysis.get("weaknesses", [])
        if weaknesses:
            for w in weaknesses:
                st.markdown(f"- {w}")
        else:
            st.info("No weaknesses data available.")

    st.divider()

    # Coach Recommendations
    with st.container():
        st.subheader("Coach Recommendations")
        recommendations = analysis.get("recommendations", [])
        if recommendations:
            for r in recommendations:
                st.markdown(f"- {r}")
        else:
            st.info("No recommendations available.")

    st.divider()

    # Final Verdict
    with st.container():
        st.subheader("Final Verdict")
        verdict = analysis.get("verdict", "")
        if verdict:
            st.markdown(f"**{verdict}**")
        else:
            st.info("Match verdict is not available.")
