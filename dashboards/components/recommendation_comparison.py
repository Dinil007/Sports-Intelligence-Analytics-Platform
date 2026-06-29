"""Executive player comparison dashboard.

Extends the original attribute comparison table with:
- Player name headers
- Interactive Plotly radar chart
- Key metric highlights
- Percentile comparison bars
- Strength/weakness comparison
- AI-powered verdict

No HTML. No CSS. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from dashboards.components.player_radar_chart import render_player_radar
from dashboards.components.player_strength_comparison import render_strength_comparison
from services.comparison_ai_service import generate_comparison_verdict


def _n(value: Any) -> float:
    try:
        return float(value) if value is not None else 0.0
    except (TypeError, ValueError):
        return 0.0


def render_recommendation_comparison(
    selected_player: dict[str, Any],
    recommended_player: dict[str, Any],
    comparison_index: int = 0,
) -> None:
    """
    Render the full executive comparison dashboard.

    Parameters
    ----------
    selected_player : dict[str, Any]
    recommended_player : dict[str, Any]
    """
    st.title("PLAYER COMPARISON")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Selected Player")
        st.markdown(f"**{selected_player.get('player_name', 'Unknown')}**")
    with col2:
        st.subheader("Recommended Player")
        st.markdown(f"**{recommended_player.get('player_name', 'Unknown')}**")

    st.divider()

    try:
        render_player_radar(selected_player, recommended_player, comparison_index=comparison_index)
    except Exception as e:
        st.exception(e)

    st.divider()

    st.subheader("Attribute Comparison")
    rows = [
        ("SPORTA Score", selected_player.get("sporta_score"), recommended_player.get("sporta_score")),
        ("Similarity", selected_player.get("similarity_pct"), recommended_player.get("similarity_pct")),
        ("Goals", selected_player.get("goals"), recommended_player.get("goals")),
        ("xG", selected_player.get("total_xg"), recommended_player.get("total_xg")),
        ("Passes", selected_player.get("passes"), recommended_player.get("passes")),
        ("Pass Accuracy", selected_player.get("pass_accuracy"), recommended_player.get("pass_accuracy")),
        ("Dribbles", selected_player.get("dribbles"), recommended_player.get("dribbles")),
        ("Carries", selected_player.get("carries"), recommended_player.get("carries")),
        ("Recoveries", selected_player.get("recoveries"), recommended_player.get("recoveries")),
        ("Pressures", selected_player.get("pressures"), recommended_player.get("pressures")),
        ("Minutes Played", selected_player.get("minutes_played"), recommended_player.get("minutes_played")),
    ]
    data = [
        {"Metric": metric, "Selected Player": sv, "Recommended Player": rv}
        for metric, sv, rv in rows
    ]
    st.dataframe(data, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader("Percentile Comparison")
    percentile_metrics = [
        ("SPORTA", "sporta_score"),
        ("Goals", "goals"),
        ("Passes", "passes"),
        ("Pressures", "pressures"),
        ("Recoveries", "recoveries"),
    ]
    for label, key in percentile_metrics:
        sv = _n(selected_player.get(key))
        rv = _n(recommended_player.get(key))
        peak = max(sv, rv, 1.0)
        sp = min(100.0, (sv / peak) * 100.0)
        rp = min(100.0, (rv / peak) * 100.0)
        st.markdown(f"**{label}**")
        c1, c2 = st.columns(2)
        with c1:
            st.caption("Selected")
            st.progress(sp / 100.0)
        with c2:
            st.caption("Recommended")
            st.progress(rp / 100.0)

    st.divider()

    try:
        render_strength_comparison(selected_player, recommended_player)
    except Exception as e:
        st.exception(e)

    st.divider()

    try:
        verdict = generate_comparison_verdict(selected_player, recommended_player)
    except Exception as e:
        verdict = {}
        st.exception(e)

    st.subheader("AI Comparison Verdict")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Winner", verdict.get("winner", "N/A"))
    with c2:
        conf = verdict.get("confidence", 0.0)
        try:
            conf = float(conf)
        except (TypeError, ValueError):
            conf = 0.0
        st.metric("Confidence", f"{conf:.0f}%")
    with c3:
        st.metric("Risk", verdict.get("risk", "Unavailable"))

    st.markdown("#### Strengths")
    for s in verdict.get("strengths", []):
        if s:
            st.markdown(f"✓ {s}")

    st.markdown("#### Weaknesses")
    for w in verdict.get("weaknesses", []):
        if w:
            st.markdown(f"• {w}")

    st.markdown("#### Final Verdict")
    st.markdown(verdict.get("verdict", "Unavailable"))

