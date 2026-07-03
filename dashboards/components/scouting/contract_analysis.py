from __future__ import annotations

import streamlit as st

from services.scouting_service import analyze_contract_status


def render_contract_analysis() -> None:
    st.header("Contract Analysis")
    player_name = st.session_state.get("scouting_selected_player")
    if not player_name:
        st.info("Select a player to review contract placeholders.")
        return
    data = analyze_contract_status(player_name)
    c1, c2, c3 = st.columns(3)
    c1.metric("Contract Remaining", data.get("contract_remaining", "Unavailable"))
    c2.metric("Renewal Priority", data.get("renewal_priority", "Medium"))
    c3.metric("Transfer Risk", data.get("transfer_risk", "Monitor"))
    st.caption(data.get("note", "Contract data unavailable."))
