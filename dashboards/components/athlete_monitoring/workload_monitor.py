from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.athlete_monitoring_service import calculate_workload


def render_workload_monitor() -> None:
    st.header("Workload Monitor")
    frames = []
    for window, rows in calculate_workload().items():
        frame = pd.DataFrame(rows)
        frame["Window"] = window
        frames.append(frame)
    df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    if df.empty:
        st.info("No workload data is available.")
        return
    fig = px.line(df, x="Period", y="Value", color="Window", markers=True)
    st.plotly_chart(fig, use_container_width=True)
