"""
dashboards/pages/11_⚽_Match_Intelligence.py
=============================================
Executive Match Intelligence dashboard.

Backend (unchanged):
    database/match_repository.py
    ml/match_metrics.py
    services/match_intelligence_service.py
"""

from __future__ import annotations

import streamlit as st

from auth.streamlit_auth import is_authenticated
from services.match_intelligence_service import get_match_dashboard

from dashboards.components.match_intelligence.match_header import render_match_header
from dashboards.components.match_intelligence.match_kpis import render_match_kpis
from dashboards.components.match_intelligence.match_team_statistics import (
    render_match_team_statistics,
)
from dashboards.components.match_intelligence.match_timeline import render_match_timeline
from dashboards.components.match_intelligence.match_player_statistics import (
    render_match_player_statistics,
)
from dashboards.components.match_intelligence.match_events import render_match_events
from dashboards.components.match_visualizations.match_dashboard import (
    render_match_dashboard,
)
from dashboards.components.pitch_visualizations.pitch_dashboard import (
    render_pitch_dashboard,
)
from dashboards.components.tactical_analysis.tactical_dashboard import (
    render_tactical_dashboard,
)

if not is_authenticated():
    st.stop()

st.title("Match Intelligence")

matches = []
try:
    from database.match_repository import fetch_matches
    matches = fetch_matches()
except Exception as e:
    st.error(f"Failed to load matches: {e}")

if not matches:
    st.info("No matches found in the database.")
else:
    match_labels = [
        f"{m['match_date']} — {m['home_team']} vs {m['away_team']} ({m.get('competition_name', '')})"
        for m in matches
    ]
    selected_label = st.selectbox("Select Match", match_labels)
    selected_idx = match_labels.index(selected_label)
    selected_match = matches[selected_idx]
    match_id = selected_match["match_id"]

    data = get_match_dashboard(match_id)

    render_match_header(data)
    st.divider()

    render_match_kpis(data)
    st.divider()

    render_match_dashboard(data)
    st.divider()

    render_pitch_dashboard(data)
    st.divider()

    render_tactical_dashboard(data)
    st.divider()

    render_match_team_statistics(data)
    st.divider()

    render_match_timeline(data)
    st.divider()

    render_match_player_statistics(data)
    st.divider()

    render_match_events(data)
