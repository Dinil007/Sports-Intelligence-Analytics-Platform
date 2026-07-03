from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.athlete_monitoring_service import calculate_sprint_metrics


def render_sprint_analysis() -> None:
    st.header("Sprint Analysis")
    df = pd.DataFrame(calculate_sprint_metrics())
    fig = px.bar(df, x="Metric", y="Value", color="Metric")
    st.plotly_chart(fig, use_container_width=True)
