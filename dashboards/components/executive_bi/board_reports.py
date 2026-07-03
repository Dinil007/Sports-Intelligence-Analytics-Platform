"""Board reports generation component."""

from __future__ import annotations

import streamlit as st
from services.executive_bi_service import generate_board_report

def render_board_reports() -> None:
    """Render board report options and deterministic output reports."""
    st.write("Generate detailed deterministic operational report documents for board meetings.")
    
    report_type = st.selectbox(
        "Select Board Report Horizon:",
        options=["monthly", "quarterly", "season"],
        format_func=lambda x: f"Generate {x.capitalize()} Report"
    )
    
    report_data = generate_board_report(report_type)
    
    st.info(f"📄 **{report_data['title']}** (As of {report_data['generated_at'][:10]})")
    for bullet in report_data["bullets"]:
        st.markdown(f"- {bullet}")
