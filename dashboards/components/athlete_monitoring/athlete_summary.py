from __future__ import annotations

import streamlit as st

from services.athlete_monitoring_service import generate_athlete_summary


def render_athlete_summary() -> None:
    st.header("Athlete Summary")
    for insight in generate_athlete_summary():
        st.write(f"- {insight}")
