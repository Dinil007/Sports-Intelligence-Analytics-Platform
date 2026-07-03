from __future__ import annotations

import pandas as pd
import streamlit as st

from services.scouting_service import analyze_squad_depth


def render_squad_gap_analysis() -> None:
    st.header("Squad Gap Analysis")
    players = st.session_state.get("scouting_filtered_players") or []
    data = analyze_squad_depth(players)
    c1, c2, c3 = st.columns(3)
    c1.metric("Average Age", data.get("average_age", 0))
    c2.metric("Recruitment Priority", data.get("recruitment_priority", "Medium"))
    c3.metric("Weak Positions", len(data.get("weak_positions", [])))
    depth = data.get("depth", [])
    if depth:
        st.dataframe(pd.DataFrame(depth), use_container_width=True, hide_index=True)
