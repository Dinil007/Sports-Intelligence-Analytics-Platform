"""
dashboards/components/match_intelligence/match_team_statistics.py
==================================================================
Team statistics comparison table for Match Intelligence.

Pure Streamlit. No charts. No HTML. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import streamlit as st


def render_match_team_statistics(data: dict[str, Any]) -> None:
    """Render a team statistics comparison table.

    Parameters
    ----------
    data : dict
        Dashboard data from ``get_match_dashboard()``.
    """
    team_stats = data.get("team_statistics", {})
    repo = team_stats.get("repository", {})

    if not repo:
        st.info("No team statistics available.")
        return

    # Collect metrics from repository stats
    home = repo.get("home_team", "Home")
    away = repo.get("away_team", "Away")

    rows = [
        ("Goals", repo.get("home_goals") or 0, repo.get("away_goals") or 0),
        ("Possession", repo.get("home_possession_avg"), repo.get("away_possession_avg")),
        ("Pass Accuracy", None, None),
        ("xG", 0.0, 0.0),
        ("Shots", repo.get("home_shots") or 0, repo.get("away_shots") or 0),
        ("PPDA", None, None),
        ("Pressures", repo.get("home_pressures") or 0, repo.get("away_pressures") or 0),
        ("Progressive Passes",
         repo.get("home_progressive_passes") or 0,
         repo.get("away_progressive_passes") or 0),
    ]

    # Also try metrics key
    metrics = team_stats.get("metrics", {})
    if home in metrics:
        hm = metrics[home]
        rows[0] = ("Goals", hm.get("goals", 0), metrics.get(away, {}).get("goals", 0))
        rows[4] = ("Shots", hm.get("shots", 0), metrics.get(away, {}).get("shots", 0))
        rows[6] = ("Pressures", hm.get("pressures", 0), metrics.get(away, {}).get("pressures", 0))
        rows[7] = ("Progressive Passes", hm.get("passes", 0), metrics.get(away, {}).get("passes", 0))

    # Overlay with ML-computed metrics if available
    pos = team_stats.get("possession", {})
    if home in pos:
        rows[1] = ("Possession", pos.get(home), pos.get(away))

    ppda = team_stats.get("ppda", {})
    if home in ppda:
        rows[5] = ("PPDA", ppda.get(home), ppda.get(away))

    display_rows = []
    for metric, home_val, away_val in rows:
        def fmt(v):
            if v is None:
                return "N/A"
            try:
                return f"{float(v):.1f}" if isinstance(v, float) else str(int(v))
            except (TypeError, ValueError):
                return str(v)
        display_rows.append({
            "Metric": metric,
            home: fmt(home_val),
            away: fmt(away_val),
        })

    st.dataframe(
        display_rows,
        use_container_width=True,
        hide_index=True,
    )
