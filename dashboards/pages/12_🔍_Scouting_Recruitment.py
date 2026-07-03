from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import streamlit as st

from auth.streamlit_auth import is_authenticated
from dashboards.components.scouting.scouting_dashboard import render_scouting_dashboard
from dashboards.components.scouting.player_search import render_player_search
from dashboards.components.scouting.advanced_filters import render_advanced_filters
from dashboards.components.scouting.player_profile import render_player_profile
from dashboards.components.scouting.performance_dashboard import render_performance_dashboard
from dashboards.components.scouting.player_comparison import render_player_comparison
from dashboards.components.scouting.similar_players import render_similar_players
from dashboards.components.scouting.recruitment_score import render_recruitment_score
from dashboards.components.scouting.transfer_shortlist import render_transfer_shortlist
from dashboards.components.scouting.market_value import render_market_value
from dashboards.components.scouting.contract_analysis import render_contract_analysis
from dashboards.components.scouting.age_profile import render_age_profile
from dashboards.components.scouting.position_analysis import render_position_analysis
from dashboards.components.scouting.replacement_finder import render_replacement_finder
from dashboards.components.scouting.squad_gap_analysis import render_squad_gap_analysis
from dashboards.components.scouting.transfer_targets import render_transfer_targets
from dashboards.components.scouting.scout_report import render_scout_report
from dashboards.components.scouting.scouting_summary import render_scouting_summary

if not is_authenticated():
    st.stop()

render_scouting_dashboard()
st.divider()
render_player_search()
st.divider()
render_advanced_filters()
st.divider()
render_player_profile()
st.divider()
render_performance_dashboard()
st.divider()
render_player_comparison()
st.divider()
render_similar_players()
st.divider()
render_recruitment_score()
st.divider()
render_transfer_shortlist()
st.divider()
render_market_value()
st.divider()
render_contract_analysis()
st.divider()
render_age_profile()
st.divider()
render_position_analysis()
st.divider()
render_replacement_finder()
st.divider()
render_squad_gap_analysis()
st.divider()
render_transfer_targets()
st.divider()
render_scout_report()
st.divider()
render_scouting_summary()
