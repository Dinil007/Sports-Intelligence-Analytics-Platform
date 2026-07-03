"""Executive KPIs rendering component."""

from __future__ import annotations

import streamlit as st
from services.executive_bi_service import calculate_executive_kpis

def render_executive_kpis() -> None:
    """Render high-level KPI cards for the Executive board."""
    kpis = calculate_executive_kpis()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Revenue YTD", value=f"€{kpis['revenue_ytd']/1e6:.1f}M")
        st.metric(label="Current Wage Bill", value=f"€{kpis['current_wage_bill']/1e6:.1f}M")
        st.metric(label="Win Percentage", value=f"{kpis['win_percentage']}%")
        
    with col2:
        st.metric(label="Operating Cost YTD", value=f"€{kpis['operating_cost_ytd']/1e6:.1f}M")
        st.metric(label="Squad Market Value", value=f"€{kpis['squad_market_value']/1e6:.1f}M")
        st.metric(label="Injury Cost YTD", value=f"€{kpis['injury_cost_ytd']/1e6:.1f}M")
        
    with col3:
        st.metric(label="Profit YTD", value=f"€{kpis['profit_ytd']/1e6:.1f}M")
        st.metric(label="Average Player Value", value=f"€{kpis['average_player_value']/1e6:.1f}M")
        st.metric(label="Transfer ROI", value=f"{kpis['transfer_roi']}x")
        
    with col4:
        st.metric(label="Transfer Budget Left", value=f"€{kpis['transfer_budget_remaining']/1e6:.1f}M")
        st.metric(label="League Position", value=f"#{kpis['league_position']}")
        st.metric(label="Attendance Rate", value=f"{kpis['attendance_rate']}%")
