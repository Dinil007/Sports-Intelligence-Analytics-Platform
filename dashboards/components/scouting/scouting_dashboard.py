from __future__ import annotations

import streamlit as st


def render_scouting_dashboard() -> None:
    st.title("SCOUTING & RECRUITMENT")
    st.caption("Club-level recruitment analytics, player discovery, transfer recommendations, squad planning and scouting reports.")
    st.info("This module is isolated from match intelligence, transfer recommendation, AI chat, data access, ETL, database, authentication and API layers.")
