from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.scouting_service import analyze_position_strength


def render_position_analysis() -> None:
    st.header("Position Analysis")
    players = st.session_state.get("scouting_filtered_players") or []
    data = analyze_position_strength(players)
    if not data:
        st.info("No position data available.")
        return
    df = pd.DataFrame(data)
    st.plotly_chart(px.bar(df, x="position", y="avg_score", color="players", title="Position Strength"), use_container_width=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
