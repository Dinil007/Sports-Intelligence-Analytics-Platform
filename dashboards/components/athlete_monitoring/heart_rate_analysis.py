from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.athlete_monitoring_service import calculate_heart_rate_metrics


def render_heart_rate_analysis() -> None:
    st.header("Heart Rate Analysis")
    data = calculate_heart_rate_metrics()
    df = pd.DataFrame(data["Series"])
    if df.empty:
        st.info("No heart-rate data is available.")
        return
    long_df = df.melt(id_vars="Minute", value_vars=["Average HR", "Maximum HR", "Recovery HR"], var_name="Metric", value_name="BPM")
    fig = px.line(long_df, x="Minute", y="BPM", color="Metric", markers=True)
    st.plotly_chart(fig, use_container_width=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Average HR", data["Average HR"])
    c2.metric("Maximum HR", data["Maximum HR"])
    c3.metric("Recovery HR", data["Recovery HR"])
    st.caption(data["Data Label"])
