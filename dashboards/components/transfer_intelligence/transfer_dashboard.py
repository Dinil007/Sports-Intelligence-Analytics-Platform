from __future__ import annotations

import streamlit as st

from dashboards.components.transfer_intelligence.replacement_analysis import render_replacement_analysis
from dashboards.components.transfer_intelligence.squad_balance import render_squad_balance
from dashboards.components.transfer_intelligence.transfer_budget import render_transfer_budget
from dashboards.components.transfer_intelligence.transfer_priority import render_transfer_priority
from dashboards.components.transfer_intelligence.transfer_risk import render_transfer_risk
from dashboards.components.transfer_intelligence.transfer_roi import render_transfer_roi
from dashboards.components.transfer_intelligence.transfer_summary import render_transfer_summary
from dashboards.components.transfer_intelligence.transfer_targets import render_transfer_targets
from dashboards.components.transfer_intelligence.transfer_value_analysis import render_transfer_value_analysis
from dashboards.components.transfer_intelligence.wage_analysis import render_wage_analysis


def render_transfer_dashboard() -> None:
    st.title("Transfer Intelligence")
    st.caption("Transfer target evaluation, squad planning, market value, ROI, wages, replacements, priorities and risk.")
    render_transfer_targets()
    st.divider()
    render_transfer_value_analysis()
    st.divider()
    render_transfer_budget()
    st.divider()
    render_wage_analysis()
    st.divider()
    render_transfer_roi()
    st.divider()
    render_replacement_analysis()
    st.divider()
    render_squad_balance()
    st.divider()
    render_transfer_priority()
    st.divider()
    render_transfer_risk()
    st.divider()
    render_transfer_summary()
