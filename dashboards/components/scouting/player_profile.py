from __future__ import annotations

import streamlit as st

from services.scouting_service import get_player_profile


def render_player_profile() -> None:
    st.header("Player Profile")
    player_name = st.session_state.get("scouting_selected_player")
    if not player_name:
        st.info("Select a player to view profile.")
        return
    profile = get_player_profile(player_name)
    col_photo, col_info = st.columns([1, 3])
    with col_photo:
        st.image(profile.get("photo") or "https://placehold.co/240x240?text=Player", caption=profile.get("player_name", "Player"))
    with col_info:
        st.subheader(profile.get("player_name", "Unknown Player"))
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Nationality", profile.get("nationality", "N/A"))
        m2.metric("Age", profile.get("age", "N/A"))
        m3.metric("Club", profile.get("club", "N/A"))
        m4.metric("Position", profile.get("position", "N/A"))
        stats = st.columns(8)
        keys = ["minutes", "goals", "assists", "xg", "xa", "passes", "carries", "sporta_score"]
        labels = ["Minutes", "Goals", "Assists", "xG", "xA", "Passes", "Carries", "SPORTA"]
        for col, label, key in zip(stats, labels, keys):
            col.metric(label, profile.get(key, 0))
        stats2 = st.columns(4)
        for col, label, key in zip(stats2, ["Pressures", "Recoveries", "Tackles", "Pass Accuracy"], ["pressures", "recoveries", "tackles", "pass_accuracy"]):
            col.metric(label, profile.get(key, 0))
