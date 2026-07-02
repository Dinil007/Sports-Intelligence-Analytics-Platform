"""
dashboards/components/passing_network/formation_detector.py
============================================================
Renders detected formations from average player positions.

Plotly only. No HTML. No CSS. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from services.passing_network_service import detect_formation


def render_detected_formation(events: list[dict[str, Any]]) -> None:
    """Render the detected tactical formations for both teams.

    Parameters
    ----------
    events : list[dict]
        Passing events list.
    """
    if not events:
        st.info("No passing events available to detect formations.")
        return

    formations = detect_formation(events)
    if not formations:
        st.info("No formations detected.")
        return

    teams = list(formations.keys())
    if not teams:
        st.info("No teams found for formations.")
        return

    # Use Plotly Indicator to render detected formations side-by-side
    fig = go.Figure()

    for idx, team in enumerate(teams):
        formation = formations[team]
        
        # Position columns side-by-side using domains
        domain_x = [0.0, 0.45] if idx == 0 else [0.55, 1.0]
        
        fig.add_trace(
            go.Indicator(
                mode="number+gauge",
                value=0,  # placeholder since we want to show a title and text
                title=dict(
                    text=f"{team}<br><span style='font-size:32px; font-weight:bold; color:#10b981;'>{formation}</span>",
                    font=dict(color="white", size=18),
                ),
                domain=dict(x=domain_x, y=[0, 1]),
            )
        )

    fig.update_layout(
        title=dict(
            text="Detected Tactical Formations",
            font=dict(color="white", size=16),
            x=0.5,
            xanchor="center",
        ),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=20, r=20, t=60, b=20),
        height=220,
    )

    st.plotly_chart(fig, use_container_width=True, key="detected_formation_chart_plotly")
