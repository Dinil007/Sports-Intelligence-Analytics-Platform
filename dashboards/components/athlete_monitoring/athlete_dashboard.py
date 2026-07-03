from __future__ import annotations

import streamlit as st

from dashboards.components.athlete_monitoring.acceleration_analysis import render_acceleration_analysis
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


def render_athlete_dashboard() -> None:
    st.title("Athlete Monitoring")
    st.caption("Player workload monitoring, fatigue analysis, recovery metrics, sprint analysis, wellness scoring and performance trends.")
    render_training_load()
    st.divider()
    render_workload_monitor()
    st.divider()
    render_fatigue_analysis()
    st.divider()
    render_recovery_analysis()
    st.divider()
    render_heart_rate_analysis()
    st.divider()
    render_distance_covered()
    st.divider()
    render_sprint_analysis()
    st.divider()
    render_acceleration_analysis()
    st.divider()
    render_deceleration_analysis()
    st.divider()
    render_high_intensity_runs()
    st.divider()
    render_wellness_score()
    st.divider()
    render_readiness_score()
    st.divider()
    render_performance_trends()
    st.divider()
    render_athlete_summary()
