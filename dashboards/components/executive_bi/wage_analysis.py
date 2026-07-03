"""Wage distribution rendering component."""

from __future__ import annotations

import streamlit as st
import plotly.express as px # type: ignore
import pandas as pd
from services.executive_bi_service import calculate_wage_analysis

def render_wage_analysis() -> None:
    """Render wage share distribution across squad status tiers using a Treemap."""
    data = calculate_wage_analysis()
    
    df = pd.DataFrame({
        "Tier": data["tiers"],
        "Count": data["counts"],
        "Wage Share (€)": data["total_wage_share"]
    })
    
    fig = px.treemap(
        df,
        path=["Tier"],
        values="Wage Share (€)",
        title="Wage Distribution Share by Player Squad Tier",
        color="Wage Share (€)",
        color_continuous_scale="Viridis",
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
    )
    
    st.plotly_chart(fig, use_container_width=True)
