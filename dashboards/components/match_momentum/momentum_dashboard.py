"""
dashboards/components/match_momentum/momentum_dashboard.py
==========================================================
Master orchestrator for Match Momentum & Game Flow Analytics.
"""

from __future__ import annotations

from typing import Any
import streamlit as st

from dashboards.components.match_momentum.momentum_timeline import render_momentum_timeline
from dashboards.components.match_momentum.momentum_kpis import render_momentum_kpis
from dashboards.components.match_momentum.possession_flow import render_possession_flow
from dashboards.components.match_momentum.dangerous_attacks import render_dangerous_attacks
from dashboards.components.match_momentum.final_third_entries import render_final_third_entries
from dashboards.components.match_momentum.ball_progression import render_ball_progression
from dashboards.components.match_momentum.pressure_timeline import render_pressure_timeline
from dashboards.components.match_momentum.attacking_direction import render_attacking_direction
from dashboards.components.match_momentum.momentum_summary import render_momentum_summary


def render_match_momentum_dashboard(match_dashboard: dict[str, Any]) -> None:
    """Render the Match Momentum & Game Flow Analytics section."""
    events = match_dashboard.get("events", []) if match_dashboard else []

    st.markdown("## Match Momentum & Game Flow Analytics")

    render_momentum_timeline(events)
    st.divider()

    render_momentum_kpis(events)
    st.divider()

    render_possession_flow(events)
    st.divider()

    render_dangerous_attacks(events)
    st.divider()

    render_final_third_entries(events)
    st.divider()

    render_ball_progression(events)
    st.divider()

    render_pressure_timeline(events)
    st.divider()

    render_attacking_direction(events)
    st.divider()

    render_momentum_summary(events)
