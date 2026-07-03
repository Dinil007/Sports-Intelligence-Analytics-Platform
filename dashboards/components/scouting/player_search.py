from __future__ import annotations

import pandas as pd
import streamlit as st

from services.scouting_service import search_players


def render_player_search() -> None:
    st.header("Player Search")
    with st.form("scouting_player_search_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("Name")
            position = st.text_input("Position")
        with col2:
            club = st.text_input("Club")
            nationality = st.text_input("Nationality")
        with col3:
            competition = st.text_input("Competition")
            limit = st.number_input("Result limit", min_value=25, max_value=1000, value=250, step=25)
        submitted = st.form_submit_button("Search players", type="primary")

    if submitted or "scouting_players" not in st.session_state:
        players = search_players(name=name, club=club, competition=competition, position=position, nationality=nationality, limit=int(limit))
        st.session_state["scouting_players"] = players
        st.session_state["scouting_filtered_players"] = players

    players = st.session_state.get("scouting_players", [])
    if not players:
        st.warning("No players found for the current search.")
        return

    names = [p["player_name"] for p in players]
    selected = st.selectbox("Selected player", names, key="scouting_selected_player")
    st.dataframe(pd.DataFrame(players)[["player_name", "club", "position", "nationality", "age", "sporta_score"]], use_container_width=True, hide_index=True)
