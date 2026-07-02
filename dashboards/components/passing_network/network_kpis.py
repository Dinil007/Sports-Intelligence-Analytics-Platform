"""
dashboards/components/passing_network/network_kpis.py
======================================================
Renders passing network KPI summary cards.

Plotly only. No HTML. No CSS. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from services.passing_network_service import (
    calculate_network_metrics,
    calculate_progressive_passes,
)


def render_network_kpis(events: list[dict[str, Any]]) -> None:
    """Render Plotly-based KPI cards summarizing network characteristics.

    Parameters
    ----------
    events : list[dict]
        Passing events list.
    """
    if not events:
        st.info("No passing events available for KPIs.")
        return

    # Calculate metrics
    metrics = calculate_network_metrics(events)
    progressive_passes = calculate_progressive_passes(events)

    if not metrics:
        st.info("No KPI data calculated.")
        return

    teams = list(metrics.keys())
    selected_team = st.selectbox("Select Team for KPI Cards", teams, key="pn_kpi_team_select")

    # Get values for selected team
    team_events = [e for e in events if e.get("team_name") == selected_team]
    total_passes = len(team_events)
    prog_passes = len(progressive_passes.get(selected_team, []))
    prog_share = round((prog_passes / total_passes * 100), 1) if total_passes > 0 else 0.0

    net_density = metrics[selected_team].get("network_density", 0.0)
    avg_len = metrics[selected_team].get("avg_pass_length", 0.0)

    # Render a 4-column KPI indicator set
    fig = go.Figure()

    # Total Passes
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=total_passes,
            title=dict(text="Total Passes", font=dict(color="white", size=14)),
            domain=dict(x=[0.0, 0.22], y=[0, 1]),
            number=dict(font=dict(color="#10b981", size=32)),
        )
    )

    # Progressive Pass Share
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=prog_share,
            number=dict(suffix="%", font=dict(color="#3b82f6", size=32)),
            title=dict(text="Progressive Share", font=dict(color="white", size=14)),
            domain=dict(x=[0.26, 0.48], y=[0, 1]),
        )
    )

    # Network Density
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=net_density,
            title=dict(text="Network Density", font=dict(color="white", size=14)),
            domain=dict(x=[0.52, 0.74], y=[0, 1]),
            number=dict(font=dict(color="#eab308", size=32)),
        )
    )

    # Avg Pass Length
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=avg_len,
            number=dict(suffix=" yds", font=dict(color="#a855f7", size=32)),
            title=dict(text="Avg Pass Length", font=dict(color="white", size=14)),
            domain=dict(x=[0.78, 1.0], y=[0, 1]),
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=100,
    )

    st.plotly_chart(fig, use_container_width=True, key="pn_kpis_plotly")
