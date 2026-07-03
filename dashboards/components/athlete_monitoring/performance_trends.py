from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.athlete_monitoring_service import calculate_performance_trends


def render_performance_trends() -> None:
    st.header("Performance Trends")
    frames = []
    for source, rows in calculate_performance_trends().items():
        frame = pd.DataFrame(rows)
        frame["Source"] = source
        frames.append(frame)
    df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    if df.empty:
        st.info("No performance trend data is available.")
        return
    fig = px.line(df, x="Period", y="Value", color="Source", markers=True)
    st.plotly_chart(fig, use_container_width=True)
