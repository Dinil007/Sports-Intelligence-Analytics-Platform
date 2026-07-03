from __future__ import annotations

import streamlit as st

from services.scouting_service import generate_scouting_summary


def render_scouting_summary() -> None:
    st.header("Scouting Summary")
    players = st.session_state.get("scouting_filtered_players") or []
    st.success(generate_scouting_summary(players))
