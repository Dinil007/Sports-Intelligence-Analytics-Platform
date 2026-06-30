"""
dashboards/components/match_visualizations/match_dashboard.py
===============================================================
Orchestrator for all match visualization charts.

Extracts ``team_stats`` from the match dashboard dict and renders
each chart in the required order using a 2-column layout.

No calculations. No SQL. No ML.
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from dashboards.components.match_visualizations.possession_chart import (
    render_possession_chart,
)
from dashboards.components.match_visualizations.shot_chart import (
    render_shot_chart,
)
from dashboards.components.match_visualizations.xg_chart import (
    render_xg_chart,
)
from dashboards.components.match_visualizations.pass_accuracy_chart import (
    render_pass_accuracy_chart,
)
from dashboards.components.match_visualizations.ppda_chart import (
    render_ppda_chart,
)
from dashboards.components.match_visualizations.progressive_pass_chart import (
    render_progressive_pass_chart,
)
from dashboards.components.match_visualizations.pressure_chart import (
    render_pressure_chart,
)


def render_match_dashboard(match_dashboard: dict[str, Any]) -> None:
    """Render the match visualization dashboard.

    Parameters
    ----------
    match_dashboard : dict
        The full dashboard dict returned by ``get_match_dashboard()``.
    """
    team_stats = match_dashboard.get("team_statistics", {})

    # Row 1: Possession | Shots
    col1, col2 = st.columns(2)
    with col1:
        render_possession_chart(team_stats)
    with col2:
        render_shot_chart(team_stats)

    # Row 2: xG | Pass Accuracy
    col3, col4 = st.columns(2)
    with col3:
        render_xg_chart(team_stats)
    with col4:
        render_pass_accuracy_chart(team_stats)

    # Row 3: PPDA | Progressive Passes
    col5, col6 = st.columns(2)
    with col5:
        render_ppda_chart(team_stats)
    with col6:
        render_progressive_pass_chart(team_stats)

    # Row 4: Pressures (full width)
    render_pressure_chart(team_stats)
