from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from services.scouting_service import calculate_recruitment_score, get_player_profile


def render_recruitment_score() -> None:
    st.header("Recruitment Score")
    player_name = st.session_state.get("scouting_selected_player")
    if not player_name:
        st.info("Select a player to calculate recruitment score.")
        return
    profile = get_player_profile(player_name)
    score = calculate_recruitment_score(profile)
    st.metric("Recruitment Score", f"{score}/100")
    fig = go.Figure(go.Indicator(mode="gauge+number", value=score, gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#22c55e"}}))
    fig.update_layout(height=320)
    st.plotly_chart(fig, use_container_width=True)
