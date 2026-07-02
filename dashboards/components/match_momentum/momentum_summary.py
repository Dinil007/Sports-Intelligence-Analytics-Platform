"""Momentum summary section."""

from __future__ import annotations

from typing import Any
import streamlit as st

from services.match_momentum_service import generate_match_momentum_summary


def render_momentum_summary(events: list[dict[str, Any]]) -> None:
    """Render deterministic match momentum summary."""
    st.subheader("Momentum Summary")
    summary = generate_match_momentum_summary(events)
    if not summary:
        st.info("No match momentum summary available.")
        return
    st.markdown(summary)
