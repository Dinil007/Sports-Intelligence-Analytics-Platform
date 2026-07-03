from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.athlete_monitoring_service import calculate_distance_covered


def render_distance_covered() -> None:
    st.header("Distance Covered")
    df = pd.DataFrame(calculate_distance_covered())
    fig = px.bar(df, x="Zone", y="Distance", color="Zone")
    st.plotly_chart(fig, use_container_width=True)
