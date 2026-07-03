from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.transfer_intelligence_service import calculate_transfer_value


def render_transfer_value_analysis() -> None:
    st.header("Transfer Value Analysis")
    df = pd.DataFrame(calculate_transfer_value())
    if df.empty:
        st.info("No transfer value data is available.")
        return
    fig = px.scatter(
        df,
        x="Market Value",
        y="SPORTA Score",
        size="Age",
        color="Priority",
        hover_name="Player",
        hover_data=["Club", "Position"],
    )
    st.plotly_chart(fig, use_container_width=True)
