"""
dashboards/components/pitch_visualizations/football_pitch.py
================================================================
Reusable football pitch rendered with Plotly shapes.

No Streamlit. No HTML. No CSS. No unsafe_allow_html.

Returns a Plotly Figure.
"""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go


def render_pitch() -> go.Figure:
    """Create a standard football pitch in Plotly.

    Uses StatsBomb-style coordinate system (0–120 on x-axis, 0–80 on y-axis).

    Returns
    -------
    plotly.graph_objects.Figure
        Figure with all pitch markings.
    """
    fig = go.Figure()

    # ------------------------------------------------------------------ #
    # Pitch outline (touchlines)
    # ------------------------------------------------------------------ #
    # Outer boundary: x in [0, 120], y in [0, 80]
    fig.add_shape(
        type="rect",
        x0=0,
        y0=0,
        x1=120,
        y1=80,
        line=dict(color="white", width=3),
    )

    # ------------------------------------------------------------------ #
    # Halfway line
    # ------------------------------------------------------------------ #
    fig.add_shape(
        type="line",
        x0=60,
        y0=0,
        x1=60,
        y1=80,
        line=dict(color="white", width=2),
    )

    # ------------------------------------------------------------------ #
    # Centre circle and centre spot
    # ------------------------------------------------------------------ #
    # Centre circle radius ~9.15 m scaled to 120x80 layout (~10.45 units)
    fig.add_shape(
        type="circle",
        x0=60 - 10.45,
        y0=40 - 10.45,
        x1=60 + 10.45,
        y1=40 + 10.45,
        line=dict(color="white", width=2),
    )
    fig.add_shape(
        type="circle",
        x0=60 - 0.8,
        y0=40 - 0.8,
        x1=60 + 0.8,
        y1=40 + 0.8,
        fillcolor="white",
        line=dict(color="white", width=1),
    )

    # ------------------------------------------------------------------ #
    # Penalty boxes (left and right)
    # StatsBomb convention: penalty box extends 18 m from goal line (~20.57 units)
    # Width: 40.3 m (~45.9 units), centred at y=40 → y in ~[17.05, 62.95]
    # ------------------------------------------------------------------ #
    # Left penalty box
    fig.add_shape(
        type="rect",
        x0=0,
        y0=17.05,
        x1=18,
        y1=62.95,
        line=dict(color="white", width=2),
    )
    # Right penalty box
    fig.add_shape(
        type="rect",
        x0=102,
        y0=17.05,
        x1=120,
        y1=62.95,
        line=dict(color="white", width=2),
    )

    # ------------------------------------------------------------------ #
    # Six-yard boxes (left and right)
    # Extends 5.5 m from goal line (~6.28 units)
    # Width: 18.32 m (~20.87 units), centred at y=40 → y in ~[29.57, 50.43]
    # ------------------------------------------------------------------ #
    # Left six-yard box
    fig.add_shape(
        type="rect",
        x0=0,
        y0=29.57,
        x1=6.28,
        y1=50.43,
        line=dict(color="white", width=2),
    )
    # Right six-yard box
    fig.add_shape(
        type="rect",
        x0=113.72,
        y0=29.57,
        x1=120,
        y1=50.43,
        line=dict(color="white", width=2),
    )

    # ------------------------------------------------------------------ #
    # Goals
    # Goal width: 7.32 m (~8.35 units), centred at y=40 → y in ~[35.82, 44.18]
    # ------------------------------------------------------------------ #
    # Left goal (drawn slightly outside the pitch for visibility)
    fig.add_shape(
        type="rect",
        x0=-2.5,
        y0=35.82,
        x1=0,
        y1=44.18,
        line=dict(color="white", width=2),
        fillcolor="rgba(255, 255, 255, 0.1)",
    )
    # Right goal
    fig.add_shape(
        type="rect",
        x0=120,
        y0=35.82,
        x1=122.5,
        y1=44.18,
        line=dict(color="white", width=2),
        fillcolor="rgba(255, 255, 255, 0.1)",
    )

    # ------------------------------------------------------------------ #
    # Penalty spots
    # 11 m from goal line (~12.57 units), centred at y=40
    # ------------------------------------------------------------------ #
    fig.add_shape(
        type="circle",
        x0=12.57 - 0.5,
        y0=40 - 0.5,
        x1=12.57 + 0.5,
        y1=40 + 0.5,
        fillcolor="white",
        line=dict(color="white", width=1),
    )
    fig.add_shape(
        type="circle",
        x0=107.43 - 0.5,
        y0=40 - 0.5,
        x1=107.43 + 0.5,
        y1=40 + 0.5,
        fillcolor="white",
        line=dict(color="white", width=1),
    )

    # ------------------------------------------------------------------ #
    # Layout
    # ------------------------------------------------------------------ #
    fig.update_layout(
        xaxis=dict(
            range=[-5, 125],
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            scaleanchor="y",
            scaleratio=68 / 80,
        ),
        yaxis=dict(
            range=[-15, 95],
            showgrid=False,
            showticklabels=False,
            zeroline=False,
        ),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=0, r=0, t=0, b=0),
        width=900,
        height=500,
        dragmode=False,
    )
    # Force a dark background behind the shapes
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)

    # Add a dark rectangle behind everything so the pitch is visible
    fig.add_shape(
        type="rect",
        x0=0,
        y0=0,
        x1=120,
        y1=80,
        fillcolor="#1a472a",
        layer="below",
        line=dict(width=0),
    )

    return fig
