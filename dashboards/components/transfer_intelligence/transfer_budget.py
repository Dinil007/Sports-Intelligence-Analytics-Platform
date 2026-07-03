from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from services.transfer_intelligence_service import calculate_transfer_budget


def render_transfer_budget() -> None:
    st.header("Transfer Budget")
    budget = calculate_transfer_budget()
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=budget["Budget Used %"],
            title={"text": "Budget Used"},
            gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#2563eb"}},
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Available Budget", f"EUR {budget['Available Budget']:,.0f}")
    c2.metric("Budget Used", f"EUR {budget['Budget Used']:,.0f}")
    c3.metric("Remaining Budget", f"EUR {budget['Remaining Budget']:,.0f}")
