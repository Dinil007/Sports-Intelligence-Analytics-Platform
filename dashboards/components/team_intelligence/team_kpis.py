"""Team KPI cards."""

from __future__ import annotations

from typing import Any

import streamlit as st

from services.team_intelligence_service import calculate_team_kpis


def render_team_kpis(events: list[dict[str, Any]]) -> None:
    """Render team KPI cards."""
    st.markdown("### Team KPIs")
    kpis = calculate_team_kpis(events)
    if not kpis:
        st.info("No team KPI data available.")
        return

    labels = [
        "Possession %",
        "Pass Accuracy",
        "Progressive Passes",
        "Progressive Carries",
        "Final Third Entries",
        "Shot Conversion",
        "Pressures",
        "Recoveries",
        "Defensive Actions",
        "Expected Threat",
    ]
    for team, values in kpis.items():
        st.caption(team)
        columns = st.columns(5)
        for index, label in enumerate(labels):
            value = values.get(label, 0)
            suffix = "%" if label in {"Possession %", "Pass Accuracy", "Shot Conversion"} else ""
            columns[index % 5].metric(label, f"{value}{suffix}")
