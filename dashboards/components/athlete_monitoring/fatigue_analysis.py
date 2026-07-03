from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from services.athlete_monitoring_service import calculate_fatigue_score


def render_fatigue_analysis() -> None:
    st.header("Fatigue Analysis")
    data = calculate_fatigue_score()
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=data["Fatigue Score"],
            title={"text": data["Band"]},
            gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#ef4444"}},
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(data["Data Label"])
