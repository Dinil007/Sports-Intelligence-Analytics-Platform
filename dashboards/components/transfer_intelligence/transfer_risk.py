from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.transfer_intelligence_service import calculate_transfer_risk


def render_transfer_risk() -> None:
    st.header("Transfer Risk Assessment")
    df = pd.DataFrame(calculate_transfer_risk())
    if df.empty:
        st.info("No transfer risk data is available.")
        return
    risk_columns = ["Age Risk", "Injury Risk", "Contract Risk", "Adaptation Risk", "Minutes Risk"]
    heatmap_df = df.set_index("Player")[risk_columns]
    fig = px.imshow(heatmap_df, aspect="auto", color_continuous_scale="RdYlGn_r", zmin=0, zmax=100)
    st.plotly_chart(fig, use_container_width=True)
