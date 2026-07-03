"""Team summary renderer."""

from __future__ import annotations

from typing import Any

import streamlit as st

from services.team_intelligence_service import generate_team_summary


def render_team_summary(events: list[dict[str, Any]]) -> None:
    """Render deterministic team summary insights."""
    st.markdown("### Team Summary")
    for insight in generate_team_summary(events):
        st.write(f"- {insight}")
