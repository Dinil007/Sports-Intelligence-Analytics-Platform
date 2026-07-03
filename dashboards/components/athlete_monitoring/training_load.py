from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from services.athlete_monitoring_service import calculate_training_load


def render_training_load() -> None:
    st.header("Training Load")
    data = calculate_training_load()
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=data["Acute:Chronic Ratio"],
            title={"text": "Acute:Chronic Ratio"},
            gauge={"axis": {"range": [0, 2]}, "bar": {"color": "#2563eb"}},
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Acute Load", data["Acute Load"])
    c2.metric("Chronic Load", data["Chronic Load"])
    c3.metric("Acute:Chronic Ratio", data["Acute:Chronic Ratio"])
    st.caption(data["Data Label"])
