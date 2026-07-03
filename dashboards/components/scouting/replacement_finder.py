from __future__ import annotations

import pandas as pd
import streamlit as st

from services.scouting_service import find_replacement_players


def render_replacement_finder() -> None:
    st.header("Replacement Finder")
    players = st.session_state.get("scouting_filtered_players") or st.session_state.get("scouting_players") or []
    names = [p["player_name"] for p in players]
    if not names:
        st.info("Search players before finding replacements.")
        return
    default_name = st.session_state.get("scouting_selected_player", names[0])
    index = names.index(default_name) if default_name in names else 0
    player_name = st.selectbox("Player to replace", names, index=index, key="scouting_replacement_player")
    replacements = find_replacement_players(player_name, limit=10)
    if replacements:
        st.dataframe(pd.DataFrame(replacements)[["player_name", "club", "position", "age", "sporta_score", "similarity"]], use_container_width=True, hide_index=True)
    else:
        st.warning("No replacement players found.")
