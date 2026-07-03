from __future__ import annotations

import streamlit as st

from services.transfer_intelligence_service import generate_transfer_summary


def render_transfer_summary() -> None:
    st.header("Executive Summary")
    for insight in generate_transfer_summary():
        st.write(f"- {insight}")
