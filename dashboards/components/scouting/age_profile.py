from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.scouting_service import analyze_age_profile


def render_age_profile() -> None:
    st.header("Age Profile")
    players = st.session_state.get("scouting_filtered_players") or []
    profile = analyze_age_profile(players)
    df = pd.DataFrame({"age_group": list(profile.keys()), "players": list(profile.values())})
    st.plotly_chart(px.bar(df, x="age_group", y="players", title="Age Group Distribution"), use_container_width=True)
