"""
dashboards/components/transfer_advisor.py
=========================================
Render the AI Transfer Advisor using native Streamlit components.

No HTML.
No unsafe_allow_html.
No custom CSS.
"""

from __future__ import annotations

from typing import Any

import streamlit as st


def render_transfer_advisor(advisor: dict[str, Any]) -> None:
    """
    Render the AI Transfer Advisor panel.

    Parameters
    ----------
    advisor : dict[str, Any]
        Structured dict returned by services/transfer_advisor_service.py.
    """
    st.subheader("🤖 AI Transfer Advisor")
    st.divider()

    if not advisor:
        st.info("AI Transfer Advisor unavailable.")
        return

    best = advisor.get("best_replacement") or "Unknown"

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Best Replacement", best)
    with col2:
        score = advisor.get("recommendation_score", 0.0)
        try:
            score = float(score)
        except (TypeError, ValueError):
            score = 0.0
        st.metric("Recommendation Score", f"{score:.1f}")
    with col3:
        conf = advisor.get("confidence", 0.0)
        try:
            conf = float(conf)
        except (TypeError, ValueError):
            conf = 0.0
        st.metric("Confidence", f"{conf:.0%}")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("Estimated Transfer Fee", advisor.get("estimated_transfer_fee", "Unknown"))
    with col5:
        st.metric("Transfer Risk", advisor.get("transfer_risk", "Unknown"))
    with col6:
        st.metric("Development Potential", advisor.get("development_potential", "Unknown"))

    col7, col8 = st.columns(2)
    with col7:
        st.metric("Contract Suitability", advisor.get("contract_suitability", "Unknown"))
    with col8:
        st.metric("Tactical Fit", advisor.get("tactical_fit", "Unknown"))

    st.divider()

    st.markdown("### Tactical Fit")
    st.markdown(advisor.get("tactical_fit", "Unavailable"))

    st.divider()

    st.markdown("### Why This Player?")
    reasons = advisor.get("top_reasons", [])
    for reason in reasons:
        if reason:
            st.markdown(f"✓ {reason}")

    st.divider()

    st.markdown("### Alternative Targets")
    alternatives = advisor.get("alternative_targets", [])
    for alt in alternatives:
        if alt:
            st.markdown(f"• {alt}")

    st.divider()

    st.markdown("### Recruitment Priority")
    st.markdown(advisor.get("recruitment_priority", "★☆☆☆☆"))

    st.divider()

    st.markdown("### Final Verdict")
    st.markdown(advisor.get("final_verdict", "Unavailable"))
