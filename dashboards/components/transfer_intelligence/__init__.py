"""Transfer Intelligence dashboard components."""

from dashboards.components.transfer_intelligence.replacement_analysis import render_replacement_analysis
from dashboards.components.transfer_intelligence.squad_balance import render_squad_balance
from dashboards.components.transfer_intelligence.transfer_budget import render_transfer_budget
from dashboards.components.transfer_intelligence.transfer_dashboard import render_transfer_dashboard
from dashboards.components.transfer_intelligence.transfer_priority import render_transfer_priority
from dashboards.components.transfer_intelligence.transfer_risk import render_transfer_risk
from dashboards.components.transfer_intelligence.transfer_roi import render_transfer_roi
from dashboards.components.transfer_intelligence.transfer_summary import render_transfer_summary
from dashboards.components.transfer_intelligence.transfer_targets import render_transfer_targets
from dashboards.components.transfer_intelligence.transfer_value_analysis import render_transfer_value_analysis
from dashboards.components.transfer_intelligence.wage_analysis import render_wage_analysis

__all__ = [
    "render_transfer_dashboard",
    "render_transfer_targets",
    "render_transfer_value_analysis",
    "render_transfer_budget",
    "render_wage_analysis",
    "render_transfer_roi",
    "render_replacement_analysis",
    "render_squad_balance",
    "render_transfer_priority",
    "render_transfer_risk",
    "render_transfer_summary",
]
