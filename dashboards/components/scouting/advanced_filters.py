from __future__ import annotations

import pandas as pd
import streamlit as st

from services.scouting_service import filter_players


def render_advanced_filters() -> None:
    st.header("Advanced Filters")
    with st.expander("Recruitment KPI filters", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            age = st.slider("Age", 15, 45, (16, 35))
            minutes_min = st.number_input("Minutes min", min_value=0, value=0, step=90)
            goals_min = st.number_input("Goals min", min_value=0.0, value=0.0, step=1.0)
        with c2:
            assists_min = st.number_input("Assists min", min_value=0.0, value=0.0, step=1.0)
            xg_min = st.number_input("xG min", min_value=0.0, value=0.0, step=0.5)
            xa_min = st.number_input("xA min", min_value=0.0, value=0.0, step=0.5)
        with c3:
            pass_accuracy_min = st.slider("Pass Accuracy min", 0, 100, 0)
            progressive_passes_min = st.number_input("Progressive Passes min", min_value=0.0, value=0.0, step=5.0)
            progressive_carries_min = st.number_input("Progressive Carries min", min_value=0.0, value=0.0, step=5.0)
        with c4:
            pressures_min = st.number_input("Pressures min", min_value=0.0, value=0.0, step=5.0)
            recoveries_min = st.number_input("Recoveries min", min_value=0.0, value=0.0, step=5.0)
            tackles_min = st.number_input("Tackles min", min_value=0.0, value=0.0, step=2.0)
            sporta_score_min = st.slider("SPORTA Score min", 0, 100, 0)

    filters = {
        "age_min": age[0], "age_max": age[1],
        "minutes_min": minutes_min,
        "goals_min": goals_min,
        "assists_min": assists_min,
        "xg_min": xg_min,
        "xa_min": xa_min,
        "pass_accuracy_min": pass_accuracy_min,
        "progressive_passes_min": progressive_passes_min,
        "progressive_carries_min": progressive_carries_min,
        "pressures_min": pressures_min,
        "recoveries_min": recoveries_min,
        "tackles_min": tackles_min,
        "sporta_score_min": sporta_score_min,
    }
    players = filter_players(filters, limit=500)
    st.session_state["scouting_filtered_players"] = players
    st.caption(f"{len(players)} players match advanced filters.")
    if players:
        st.dataframe(pd.DataFrame(players)[["player_name", "position", "age", "minutes", "goals", "assists", "xg", "xa", "pass_accuracy", "sporta_score"]], use_container_width=True, hide_index=True)
