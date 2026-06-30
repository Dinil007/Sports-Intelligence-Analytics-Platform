"""
dashboards/components/match_intelligence/match_kpis.py
========================================================
KPI strip for Match Intelligence.

Uses only ``st.metric``.
No charts. No HTML. No CSS.
"""

from __future__ import annotations

from typing import Any

import streamlit as st


def render_match_kpis(data: dict[str, Any]) -> None:
    """Render key performance indicators for the match.

    Parameters
    ----------
    data : dict
        Dashboard data from ``get_match_dashboard()``.
    """
    score = data.get("score", {})
    home_goals = score.get("home", 0)
    away_goals = score.get("away", 0)

    team_stats = data.get("team_statistics", {})

    possession = team_stats.get("possession", {})
    ppda = team_stats.get("ppda", {})
    pressures = team_stats.get("pressures", {})
    progressive_passes = team_stats.get("progressive_passes", {})
    xg = team_stats.get("xg", {})

    repo = team_stats.get("repository", {})
    home_team = repo.get("home_team", "Home")
    away_team = repo.get("away_team", "Away")

    total_shots = (repo.get("home_shots") or 0) + (repo.get("away_shots") or 0)
    total_pressures = (pressures.get(home_team) or 0) + (pressures.get(away_team) or 0)
    total_prog_passes = (
        (progressive_passes.get(home_team) or 0) + (progressive_passes.get(away_team) or 0)
    )

    ppda_vals = [v for v in ppda.values() if v is not None]
    ppda_avg = sum(ppda_vals) / len(ppda_vals) if ppda_vals else None

    def fmt(v, suffix=""):
        if v is None:
            return "N/A"
        try:
            return f"{v:.1f}{suffix}" if isinstance(v, float) else f"{int(v)}{suffix}"
        except (TypeError, ValueError):
            return str(v)

    row1 = st.columns(4)
    kpis1 = [
        ("Goals", f"{home_goals} – {away_goals}"),
        ("Shots", fmt(total_shots)),
        ("Pressures", fmt(total_pressures)),
        ("Progressive Passes", fmt(total_prog_passes)),
    ]
    for col, (label, value) in zip(row1, kpis1):
        with col:
            st.metric(label, value)

    row2 = st.columns(4)
    kpis2 = [
        ("xG", fmt(sum(v for v in xg.values() if v is not None))),
        ("Pass Accuracy", "N/A"),
        ("PPDA", fmt(ppda_avg)),
        ("Possession", fmt(None)),
    ]
    for col, (label, value) in zip(row2, kpis2):
        with col:
            st.metric(label, value)
