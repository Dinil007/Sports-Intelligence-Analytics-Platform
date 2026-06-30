"""
dashboards/components/visualizations/recommendation_dashboard.py
================================================================
Main orchestrator that renders all four recommendation visualisations
in a vertical layout.  No HTML, no CSS, no unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from dashboards.components.visualizations.recommendation_similarity_chart import (
    render_similarity_chart,
)
from dashboards.components.visualizations.recommendation_sporta_chart import (
    render_sporta_score_chart,
)
from dashboards.components.visualizations.recommendation_xg_chart import (
    render_xg_chart,
)
from dashboards.components.visualizations.recommendation_goal_chart import (
    render_goal_contribution_chart,
)


def render_recommendation_dashboard(recommendations: list[dict[str, Any]]) -> None:
    """Render the full recommendation analytics dashboard.

    Layout
    ------
    1. Similarity %  (horizontal bar)
    2. SPORTA Score  (vertical bar)
    3. xG            (horizontal bar)
    4. Goal Contribution  (grouped bar)

    Parameters
    ----------
    recommendations : list[dict[str, Any]]
        Enriched player dicts from the recommendation service.
    """
    if not recommendations:
        st.info("No recommendation data available for visualizations.")
        return

    st.subheader("Recommendation Analytics")
    st.divider()

    render_similarity_chart(recommendations)
    st.divider()

    render_sporta_score_chart(recommendations)
    st.divider()

    render_xg_chart(recommendations)
    st.divider()

    render_goal_contribution_chart(recommendations)
    st.divider()
