from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.transfer_intelligence_service import calculate_wage_structure


def render_wage_analysis() -> None:
    st.header("Wage Analysis")
    df = pd.DataFrame(calculate_wage_structure())
    if df.empty:
        st.info("No wage structure data is available.")
        return
    fig = px.bar(df.sort_values("Weekly Wage"), x="Weekly Wage", y="Player", orientation="h", color="Priority")
    st.plotly_chart(fig, use_container_width=True)
