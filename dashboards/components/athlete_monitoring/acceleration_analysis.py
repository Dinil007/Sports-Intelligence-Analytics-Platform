from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.athlete_monitoring_service import calculate_acceleration_metrics


def render_acceleration_analysis() -> None:
    st.header("Acceleration Analysis")
    df = pd.DataFrame(calculate_acceleration_metrics())
    fig = px.histogram(df, x="Zone", y="Count", color="Zone", histfunc="sum")
    st.plotly_chart(fig, use_container_width=True)
