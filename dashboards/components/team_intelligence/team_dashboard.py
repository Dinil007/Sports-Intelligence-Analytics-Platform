"""Team Intelligence dashboard orchestrator."""

from __future__ import annotations

from typing import Any

import streamlit as st

from dashboards.components.team_intelligence.build_up_play import render_build_up_play
from dashboards.components.team_intelligence.expected_threat import render_expected_threat
from dashboards.components.team_intelligence.formation_analysis import render_formation_analysis
from dashboards.components.team_intelligence.playing_style import render_playing_style
from dashboards.components.team_intelligence.possession_chains import render_possession_chains
from dashboards.components.team_intelligence.pressing_analysis import render_pressing_analysis
from dashboards.components.team_intelligence.team_kpis import render_team_kpis
from dashboards.components.team_intelligence.team_similarity import render_team_similarity
from dashboards.components.team_intelligence.team_summary import render_team_summary
from dashboards.components.team_intelligence.zone_dominance import render_zone_dominance


def render_team_intelligence_dashboard(match_dashboard: dict[str, Any]) -> None:
    """Render Team Intelligence & Tactical Pattern Analysis."""
    events = match_dashboard.get("events", []) if match_dashboard else []

    st.markdown("## Team Intelligence")

    render_team_kpis(events)
    st.divider()

    render_formation_analysis(events)
    st.divider()

    render_playing_style(events)
    st.divider()

    render_build_up_play(events)
    st.divider()

    render_possession_chains(events)
    st.divider()

    render_pressing_analysis(events)
    st.divider()

    render_zone_dominance(events)
    st.divider()

    render_expected_threat(events)
    st.divider()

    render_team_similarity(events)
    st.divider()

    render_team_summary(events)
