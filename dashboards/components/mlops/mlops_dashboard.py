"""MLOps Main Dashboard Orchestrator Component."""
from __future__ import annotations

import streamlit as st

from dashboards.components.mlops.experiment_dashboard      import render_experiment_dashboard
from dashboards.components.mlops.experiment_comparison     import render_experiment_comparison
from dashboards.components.mlops.model_registry_dashboard  import render_model_registry_dashboard
from dashboards.components.mlops.feature_store_dashboard   import render_feature_store_dashboard
from dashboards.components.mlops.feature_catalog_dashboard import render_feature_catalog
from dashboards.components.mlops.drift_dashboard           import render_drift_dashboard
from dashboards.components.mlops.retraining_dashboard      import render_retraining_dashboard, render_training_history
from dashboards.components.mlops.deployment_dashboard      import render_deployment_dashboard, render_deployment_history
from dashboards.components.mlops.prediction_monitor_dashboard import render_prediction_monitor_dashboard
from dashboards.components.mlops.model_health_dashboard    import render_model_health_dashboard
from dashboards.components.mlops.mlops_summary             import render_mlops_summary


def render_mlops_dashboard() -> None:
    """Master orchestrator — routes tabs to individual dashboard components."""
    st.markdown(
        """
        <style>
        .mlops-header {
            background: linear-gradient(135deg, rgba(14,165,233,0.14), rgba(37,99,235,0.14));
            border: 1px solid rgba(56,189,248,0.22);
            border-radius: 16px;
            padding: 1.5rem 2rem;
            margin-bottom: 1.5rem;
        }
        .mlops-header h1 { color: #f8fafc; margin: 0; font-size: 1.8rem; font-weight: 900; }
        .mlops-header p  { color: #94a3b8; margin: 0.3rem 0 0; font-size: 0.95rem; }
        </style>
        <div class="mlops-header">
            <h1>🤖 Enterprise MLOps Platform</h1>
            <p>SPORTA VISTA PRO · Production-Grade Machine Learning Operations</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tabs = st.tabs([
        "🏠 Summary",
        "🧪 Experiments",
        "🗂 Model Registry",
        "🗃 Feature Store",
        "📖 Feature Catalog",
        "🔬 Comparison",
        "📡 Drift Detection",
        "🔄 Retraining",
        "🚢 Deployment",
        "📡 Pred. Monitor",
        "💚 Model Health",
    ])

    with tabs[0]:  render_mlops_summary()
    with tabs[1]:  render_experiment_dashboard()
    with tabs[2]:  render_model_registry_dashboard()
    with tabs[3]:  render_feature_store_dashboard()
    with tabs[4]:  render_feature_catalog()
    with tabs[5]:  render_experiment_comparison()
    with tabs[6]:  render_drift_dashboard()
    with tabs[7]:  render_retraining_dashboard()
    with tabs[8]:  render_deployment_dashboard()
    with tabs[9]:  render_prediction_monitor_dashboard()
    with tabs[10]: render_model_health_dashboard()
