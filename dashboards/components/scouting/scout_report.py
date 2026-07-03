from __future__ import annotations

import pandas as pd
import streamlit as st

from services.scouting_service import generate_scout_report


def render_scout_report() -> None:
    st.header("Scout Report")
    player_name = st.session_state.get("scouting_selected_player")
    if not player_name:
        st.info("Select a player to generate a scout report.")
        return
    report = generate_scout_report(player_name)
    if not report:
        st.warning("Scout report unavailable.")
        return
    st.subheader("Overview")
    st.write(report.get("overview"))
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Technical")
        st.write(report.get("technical"))
        st.subheader("Tactical")
        st.write(report.get("tactical"))
        st.subheader("Physical")
        st.write(report.get("physical"))
    with c2:
        st.subheader("Recommendation")
        st.metric("Decision", report.get("recommendation", "Monitor"))
        st.metric("Risk Assessment", report.get("risk_assessment", "Medium"))
    st.subheader("Statistical Summary")
    st.dataframe(pd.DataFrame([report.get("statistical_summary", {})]), use_container_width=True, hide_index=True)
