"""Executive Business Intelligence component registry."""

from __future__ import annotations

from dashboards.components.executive_bi.executive_dashboard import render_executive_dashboard
from dashboards.components.executive_bi.executive_kpis import render_executive_kpis
from dashboards.components.executive_bi.financial_overview import render_financial_overview
from dashboards.components.executive_bi.commercial_analytics import render_commercial_analytics
from dashboards.components.executive_bi.revenue_analysis import render_revenue_analysis
from dashboards.components.executive_bi.expense_analysis import render_expense_analysis
from dashboards.components.executive_bi.transfer_finance import render_transfer_finance
from dashboards.components.executive_bi.wage_analysis import render_wage_analysis
from dashboards.components.executive_bi.player_roi import render_player_roi
from dashboards.components.executive_bi.contract_management import render_contract_management
from dashboards.components.executive_bi.budget_planning import render_budget_planning
from dashboards.components.executive_bi.squad_value import render_squad_value
from dashboards.components.executive_bi.attendance_analytics import render_attendance_analytics
from dashboards.components.executive_bi.fan_engagement import render_fan_engagement
from dashboards.components.executive_bi.sponsorship_analysis import render_sponsorship_analysis
from dashboards.components.executive_bi.merchandise_sales import render_merchandise_sales
from dashboards.components.executive_bi.board_reports import render_board_reports
from dashboards.components.executive_bi.executive_summary import render_executive_summary

__all__ = [
    "render_executive_dashboard",
    "render_executive_kpis",
    "render_financial_overview",
    "render_commercial_analytics",
    "render_revenue_analysis",
    "render_expense_analysis",
    "render_transfer_finance",
    "render_wage_analysis",
    "render_player_roi",
    "render_contract_management",
    "render_budget_planning",
    "render_squad_value",
    "render_attendance_analytics",
    "render_fan_engagement",
    "render_sponsorship_analysis",
    "render_merchandise_sales",
    "render_board_reports",
    "render_executive_summary",
]
