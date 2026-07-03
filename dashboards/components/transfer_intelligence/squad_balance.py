from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.transfer_intelligence_service import calculate_squad_balance


def render_squad_balance() -> None:
    st.header("Squad Balance")
    df = pd.DataFrame(calculate_squad_balance())
    long_df = df.melt(id_vars="Position Group", value_vars=["Current Squad", "Ideal Squad"], var_name="Squad", value_name="Players")
    fig = px.bar(long_df, x="Position Group", y="Players", color="Squad", barmode="stack")
    st.plotly_chart(fig, use_container_width=True)
