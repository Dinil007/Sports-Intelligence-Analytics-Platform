from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.transfer_intelligence_service import calculate_transfer_priority


def render_transfer_priority() -> None:
    st.header("Transfer Priority Matrix")
    df = pd.DataFrame(calculate_transfer_priority())
    if df.empty:
        st.info("No transfer priority data is available.")
        return
    fig = px.scatter(
        df,
        x="Market Value",
        y="SPORTA Score",
        color="Quadrant",
        size="Transfer Fit",
        hover_name="Player",
        hover_data=["Club", "Position", "Priority"],
    )
    fig.add_vline(x=8_000_000, line_dash="dash", line_color="#64748b")
    fig.add_hline(y=72, line_dash="dash", line_color="#64748b")
    st.plotly_chart(fig, use_container_width=True)
