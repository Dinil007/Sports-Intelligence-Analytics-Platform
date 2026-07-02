"""Player summary component."""

from __future__ import annotations

from typing import Any
import streamlit as st

from services.player_intelligence_service import generate_player_summary


def render_player_summary(events: list[dict[str, Any]]) -> None:
    """Render deterministic player intelligence summary."""
    st.subheader("Player Summary")
    summary = generate_player_summary(events)
    if not summary:
        st.info("No player summary available.")
        return
    st.markdown(summary)
