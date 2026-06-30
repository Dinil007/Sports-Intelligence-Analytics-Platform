"""
dashboards/components/pitch_visualizations/shot_map.py
=======================================================
Display shots on the football pitch with outcome-based symbols.

Plotly only. No HTML. No CSS. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
import streamlit as st

from dashboards.components.pitch_visualizations.football_pitch import render_pitch

# Symbol mapping by shot outcome.
_SHOT_SYMBOLS = {
    "Goal": "star",
    "Saved": "circle",
    "Blocked": "square",
    "Off Target": "x",
    "Saved to Post": "circle",
    "Saved Off Target": "circle",
    "Post": "diamond",
}

_SHOT_COLORS = {
    "Goal": "#22c55e",
    "Saved": "#fbbf24",
    "Blocked": "#f97316",
    "Off Target": "#ef4444",
    "Saved to Post": "#fbbf24",
    "Saved Off Target": "#fbbf24",
    "Post": "#8b5cf6",
}


def render_shot_map(events: list[dict[str, Any]]) -> None:
    """Render shot events on the football pitch.

    Parameters
    ----------
    events : list[dict]
        Event list from ``match_dashboard["events"]``.
    """
    if not events:
        st.info("No events available for shot map.")
        return

    shot_events = [
        e for e in events
        if e.get("event_type") == "Shot"
        and e.get("location") is not None
    ]

    if not shot_events:
        st.info("Pitch coordinates are unavailable for this event type.")
        return

    fig = render_pitch()

    for e in shot_events:
        outcome = e.get("outcome") or "Off Target"
        symbol = _SHOT_SYMBOLS.get(outcome, "x")
        color = _SHOT_COLORS.get(outcome, "#6b7280")

        # Bubble size driven by xG if present, otherwise default size.
        xg = e.get("xg")
        if xg is None:
            xg = e.get("shot_xg", 0.05)
        xg = float(xg) if xg is not None else 0.05

        fig.add_trace(
            go.Scatter(
                x=[e["location"][0]],
                y=[e["location"][1]],
                mode="markers",
                marker=dict(
                    size=max(8, xg * 80),
                    color=color,
                    symbol=symbol,
                    line=dict(width=1, color="white"),
                    opacity=0.9,
                ),
                name=f"{e.get('player_name', 'Unknown')} ({outcome})",
                hovertemplate=(
                    "Player: %{customdata[0]}<br>"
                    "Minute: %{customdata[1]}<br>"
                    "Outcome: %{customdata[2]}<br>"
                    "xG: %{customdata[3]:.3f}<extra></extra>"
                ),
                customdata=[
                    [
                        e.get("player_name"),
                        e.get("minute"),
                        outcome,
                        xg,
                    ]
                ],
                showlegend=False,
            )
        )

    fig.update_layout(
        title="Shot Map",
        width=900,
        height=500,
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True, key="match_shot_map")
