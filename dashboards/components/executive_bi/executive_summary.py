"""Executive Summary rendering component."""

from __future__ import annotations

import streamlit as st
from services.executive_bi_service import generate_executive_summary

def render_executive_summary() -> None:
    """Render executive summary bullet points."""
    bullets = generate_executive_summary()
    
    st.success("📊 **Operations Strategic Highlights**")
    for bullet in bullets:
        st.markdown(f"- {bullet}")
