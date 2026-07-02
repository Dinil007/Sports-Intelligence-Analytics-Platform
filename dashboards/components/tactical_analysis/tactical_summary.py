"""
dashboards/components/tactical_analysis/tactical_summary.py
============================================================
Renders the executive summary section.
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from services.tactical_analysis_service import generate_tactical_summary


def render_tactical_summary(match_dashboard: dict[str, Any]) -> None:
    """Render the tactical executive summary."""
    st.subheader("Executive Summary")
    summary = generate_tactical_summary(match_dashboard)
    if not summary:
        st.info("Tactical summary is not available.")
        return

    # Handle dict-based summary (structured overview + key stats)
    if isinstance(summary, dict):
        overview = summary.get("overview") or summary.get("summary") or ""
        if overview:
            st.markdown("**Overview**")
            st.markdown(overview)
        # Render key statistics if present
        stat_keys = [
            ("Total Events", "total_events"),
            ("Passes", "passes"),
            ("Shots", "shots"),
            ("Carries", "carries"),
            ("Pressures", "pressures"),
            ("Recoveries", "recoveries"),
        ]
        st.markdown("**Key Statistics**")
        for label, key in stat_keys:
            value = summary.get(key)
            if value is not None:
                st.markdown(chr(8226) + " {0}: {1}".format(label, value))
        return

    # Fallback: plain string summary
    st.markdown(summary)
