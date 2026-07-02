"""Player Intelligence dashboard orchestrator."""

from __future__ import annotations

from typing import Any
import streamlit as st

from dashboards.components.player_intelligence.player_radar import render_player_radar
from dashboards.components.player_intelligence.player_score import render_player_scores
from dashboards.components.player_intelligence.player_rankings import render_player_rankings
from dashboards.components.player_intelligence.player_comparison_chart import render_player_comparison
from dashboards.components.player_intelligence.player_influence_map import render_player_influence
from dashboards.components.player_intelligence.player_timeline import render_player_timeline
from dashboards.components.player_intelligence.player_roles import render_player_roles
from dashboards.components.player_intelligence.player_awards import render_player_awards
from dashboards.components.player_intelligence.player_summary import render_player_summary


def render_player_intelligence_dashboard(match_dashboard: dict[str, Any]) -> None:
    """Render Player Intelligence & Performance Analytics."""
    events = match_dashboard.get("events", []) if match_dashboard else []

    st.markdown("## Player Intelligence & Performance Analytics")

    render_player_radar(events)
    st.divider()

    render_player_scores(events)
    st.divider()

    render_player_rankings(events)
    st.divider()

    render_player_comparison(events)
    st.divider()

    render_player_influence(events)
    st.divider()

    render_player_timeline(events)
    st.divider()

    render_player_roles(events)
    st.divider()

    render_player_awards(events)
    st.divider()

    render_player_summary(events)
