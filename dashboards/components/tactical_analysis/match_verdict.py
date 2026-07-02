"""
dashboards/components/tactical_analysis/match_verdict.py
===========================================================
Renders the final match verdict section.
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from services.tactical_analysis_service import generate_match_verdict


def render_match_verdict(match_dashboard: dict[str, Any]) -> None:
    """Render the final match verdict."""
    st.subheader("Final Verdict")
    verdict = generate_match_verdict(match_dashboard)
    if not verdict:
        st.info("Match verdict is not available.")
        return

    if isinstance(verdict, dict):
        winner = verdict.get("winner") or ""
        if winner:
            st.markdown("### Winner")
            st.markdown(str(winner))

        score = verdict.get("score") or ""
        if score:
            st.markdown("### Predicted Score")
            st.markdown(str(score))

        reasoning = verdict.get("reasoning") or ""
        if reasoning:
            st.markdown("### Reasoning")
            st.markdown(str(reasoning))
        return

    # Fallback: plain string verdict
    st.markdown("**" + str(verdict) + "**")