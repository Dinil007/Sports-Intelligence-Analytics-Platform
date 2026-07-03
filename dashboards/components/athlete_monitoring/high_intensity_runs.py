from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.athlete_monitoring_service import calculate_high_intensity_runs


def render_high_intensity_runs() -> None:
    st.header("High Intensity Runs")
    frames = []
    for metric, rows in calculate_high_intensity_runs().items():
        frame = pd.DataFrame(rows)
        frame["Metric"] = metric
        frames.append(frame)
    df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    if df.empty:
        st.info("No high-intensity run data is available.")
        return
    fig = px.line(df, x="Period", y="Value", color="Metric", markers=True)
    st.plotly_chart(fig, use_container_width=True)
