"""Player badge components for displaying tiers and attributes."""

from __future__ import annotations

import streamlit as st


def sporta_tier(score: float) -> str:
    """Return SPORTA Tier label based on score."""
    if score >= 85:
        return "Elite"
    if score >= 70:
        return "High"
    if score >= 55:
        return "Medium"
    return "Low"


def sporta_tier_class(score: float) -> str:
    """Return CSS class for SPORTA Tier badge."""
    tier = sporta_tier(score)
    return tier.lower()


def badge_html(text: str, css_class: str) -> str:
    """Return lightweight inline HTML for a badge."""
    return f'<span class="sporta-badge {css_class}">{text}</span>'


def render_badges(player: dict) -> None:
    """
    Render SPORTA tier, position, and preferred foot badges inline.

    Uses lightweight st.markdown with inline spans.
    """
    score = player.get("sporta_score", 0)
    tier = sporta_tier(score)
    tier_cls = sporta_tier_class(score)
    position = player.get("position") or "—"
    foot = player.get("preferred_foot") or "—"

    badge_row = " ".join([
        badge_html(tier, tier_cls),
        badge_html(position, "medium"),
        badge_html(foot, "low"),
    ])
    st.markdown(badge_row, unsafe_allow_html=True)
