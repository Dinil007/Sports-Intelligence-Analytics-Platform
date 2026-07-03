"""Athlete Monitoring dashboard components."""

from dashboards.components.athlete_monitoring.acceleration_analysis import render_acceleration_analysis
from dashboards.components.athlete_monitoring.athlete_dashboard import render_athlete_dashboard
from dashboards.components.athlete_monitoring.athlete_summary import render_athlete_summary
from dashboards.components.athlete_monitoring.deceleration_analysis import render_deceleration_analysis
from dashboards.components.athlete_monitoring.distance_covered import render_distance_covered
from dashboards.components.athlete_monitoring.fatigue_analysis import render_fatigue_analysis
from dashboards.components.athlete_monitoring.heart_rate_analysis import render_heart_rate_analysis
from dashboards.components.athlete_monitoring.high_intensity_runs import render_high_intensity_runs
from dashboards.components.athlete_monitoring.performance_trends import render_performance_trends
from dashboards.components.athlete_monitoring.readiness_score import render_readiness_score
from dashboards.components.athlete_monitoring.recovery_analysis import render_recovery_analysis
from dashboards.components.athlete_monitoring.sprint_analysis import render_sprint_analysis
from dashboards.components.athlete_monitoring.training_load import render_training_load
from dashboards.components.athlete_monitoring.wellness_score import render_wellness_score
from dashboards.components.athlete_monitoring.workload_monitor import render_workload_monitor

__all__ = [
    "render_athlete_dashboard",
    "render_training_load",
    "render_workload_monitor",
    "render_fatigue_analysis",
    "render_recovery_analysis",
    "render_heart_rate_analysis",
    "render_distance_covered",
    "render_sprint_analysis",
    "render_acceleration_analysis",
    "render_deceleration_analysis",
    "render_high_intensity_runs",
    "render_wellness_score",
    "render_readiness_score",
    "render_performance_trends",
    "render_athlete_summary",
]
