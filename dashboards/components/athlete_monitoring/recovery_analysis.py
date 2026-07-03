from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from services.athlete_monitoring_service import calculate_recovery_score


def render_recovery_analysis() -> None:
    st.header("Recovery Analysis")
    data = calculate_recovery_score()
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=data["Recovery %"],
            title={"text": "Recovery %"},
            gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#22c55e"}},
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    c1, c2 = st.columns(2)
    c1.metric("Sleep Quality", data["Sleep Quality"])
    c2.metric("Recovery Index", data["Recovery Index"])
    st.caption(data["Data Label"])
