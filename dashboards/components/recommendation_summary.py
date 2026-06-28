"""Recommendation summary component for executive dashboard kpis."""

from __future__ import annotations

from typing import Any

import streamlit as st


def render_recommendation_summary(
    recommendations: list[dict[str, Any]],
    selected_player: str,
) -> None:
    """Render an executive recommendation summary above the recommendation cards.

    Parameters
    ----------
    recommendations : list[dict[str, Any]]
        Already computed recommendations from the recommendation engine.
        Each dict is expected to contain keys like ``similarity_pct``,
        ``sporta_score``, ``club``, ``age``, and ``minutes_played``.
    selected_player : str
        Display name of the reference player selected by the user.
    """
    if not recommendations:
        st.info("No recommendations available.")
        return

    st.subheader("Recommendation Summary")

    total = len(recommendations)

    similarities = [
        float(r.get("similarity_pct", 0) or 0)
        for r in recommendations
        if r.get("similarity_pct") is not None
    ]
    avg_similarity = (
        round(sum(similarities) / len(similarities), 1) if similarities else 0.0
    )

    sporta_scores = [
        float(r.get("sporta_score", 0) or 0)
        for r in recommendations
        if r.get("sporta_score") is not None
    ]
    highest_sporta = (
        round(max(sporta_scores), 1) if sporta_scores else 0.0
    )

    clubs = {r.get("club") for r in recommendations if r.get("club")}
    clubs_count = len(clubs)

    ages = [r.get("age") for r in recommendations if r.get("age") is not None]
    avg_age = (
        round(sum(ages) / len(ages), 1) if ages else None
    )

    minutes = [
        r.get("minutes_played")
        for r in recommendations
        if r.get("minutes_played") is not None
    ]
    avg_minutes = (
        round(sum(minutes) / len(minutes)) if minutes else None
    )

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric("Recommendations", f"{total}")

    with col2:
        st.metric("Average Similarity", f"{avg_similarity}%")

    with col3:
        st.metric("Highest SPORTA", f"{highest_sporta}")

    with col4:
        st.metric("Clubs", f"{clubs_count}")

    with col5:
        st.metric("Average Age", f"{avg_age if avg_age is not None else '—'}")

    with col6:
        st.metric(
            "Average Minutes",
            f"{avg_minutes if avg_minutes is not None else '—'}",
        )

    st.markdown(f"**Selected Player**\n\n{selected_player}")
    st.markdown(f"**Players Evaluated**\n\n{total}")
