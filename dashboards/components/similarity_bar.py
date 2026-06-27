"""Similarity progress bar component."""

from __future__ import annotations

import streamlit as st


def similarity_color(percentage: float) -> str:
    """Return hex color based on similarity percentage."""
    if percentage >= 85:
        return "#10b981"  # green
    if percentage >= 70:
        return "#3b82f6"  # blue
    if percentage >= 55:
        return "#f59e0b"  # amber
    return "#64748b"  # slate


def render_similarity_bar(percentage: float) -> None:
    """
    Render a similarity progress bar using native Streamlit components.

    Parameters
    ----------
    percentage : float
        Similarity score between 0 and 100.
    """
    pct = max(0.0, min(100.0, float(percentage)))
    progress_value = pct / 100.0
    color = similarity_color(pct)

    st.progress(progress_value)
    st.markdown(
        f"<span style='color: {color}; font-weight: 700;'>{pct:.1f}%</span>",
        unsafe_allow_html=True,
    )
