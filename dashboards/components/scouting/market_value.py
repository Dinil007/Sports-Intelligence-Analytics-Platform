from __future__ import annotations

import streamlit as st

from services.scouting_service import calculate_market_value


def render_market_value() -> None:
    st.header("Market Value Analysis")
    player_name = st.session_state.get("scouting_selected_player")
    if not player_name:
        st.info("Select a player to estimate market value.")
        return
    value = calculate_market_value(player_name)
    st.metric("Estimated Market Value", f"{value.get('currency', 'EUR')} {value.get('estimated_value', 0):,}")
    st.caption(f"Value band: {value.get('band', 'Unavailable')}")
    st.write("Drivers:", ", ".join(value.get("drivers", [])))
