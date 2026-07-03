from __future__ import annotations

import pandas as pd
import streamlit as st

from services.scouting_service import find_similar_players


def render_similar_players() -> None:
    st.header("Similar Players")
    player_name = st.session_state.get("scouting_selected_player")
    if not player_name:
        st.info("Select a player to find similar profiles.")
        return
    similar = find_similar_players(player_name, limit=10)
    if not similar:
        st.warning("No similar players found.")
        return
    st.dataframe(pd.DataFrame(similar)[["player_name", "club", "position", "age", "sporta_score", "similarity"]], use_container_width=True, hide_index=True)
