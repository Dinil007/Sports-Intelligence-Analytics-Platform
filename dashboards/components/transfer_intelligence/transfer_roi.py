from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.transfer_intelligence_service import calculate_transfer_roi


def render_transfer_roi() -> None:
    st.header("Transfer ROI")
    df = pd.DataFrame(calculate_transfer_roi())
    if df.empty:
        st.info("No transfer ROI data is available.")
        return
    fig = px.scatter(
        df,
        x="Transfer Cost",
        y="Performance Score",
        size="ROI",
        color="Priority",
        hover_name="Player",
        hover_data=["Club", "Position", "Market Value"],
    )
    st.plotly_chart(fig, use_container_width=True)
