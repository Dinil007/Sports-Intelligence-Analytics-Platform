"""Final third entries chart."""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from services.match_momentum_service import calculate_final_third_entries


def render_final_third_entries(events: list[dict[str, Any]]) -> None:
    """Render entries into the attacking third."""
    st.subheader("Final Third Entries")
    if not events:
        st.info("No event data available for final third entries.")
        return

    entries = calculate_final_third_entries(events)
    if not entries:
        st.info("No final third entries calculated.")
        return

    teams = list(entries.keys())
    values = [entries[team] for team in teams]

    fig = go.Figure(
        go.Bar(
            x=teams,
            y=values,
            marker=dict(color="#10b981", line=dict(color="white", width=1)),
            text=values,
            textposition="auto",
            hovertemplate="Team: %{x}<br>Final Third Entries: %{y}<extra></extra>",
        )
    )
    fig.update_layout(
        title_text="Entries into the Attacking Third",
        xaxis_title="Team",
        yaxis_title="Entries",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color="white"),
        margin=dict(l=40, r=20, t=60, b=50),
        height=320,
    )
    fig.update_yaxes(gridcolor="rgba(255, 255, 255, 0.1)")

    st.plotly_chart(fig, use_container_width=True, key="match_momentum_final_third_entries_plotly")
