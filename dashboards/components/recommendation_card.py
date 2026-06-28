"""Recommendation card component for scouting results.

Renders directly using native Streamlit widgets.
No HTML templates or strings returned.
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from dashboards.components.action_buttons import render_action_buttons
from dashboards.components.metric_chip import format_kpi, render_metrics
from dashboards.components.player_badges import render_badges
from dashboards.components.similarity_bar import render_similarity_bar
from services.scout_report_service import generate_scout_report


def render_recommendation_card(player: dict[str, Any]) -> None:
    """
    Render a single recommendation card using native Streamlit components.

    Parameters
    ----------
    player : dict[str, Any]
        Enriched player dictionary containing display-ready fields:
        player_name, club, nationality, position, age, minutes_played,
        sporta_score, similarity_pct, goals, assists, total_xg, passes,
        pass_accuracy, dribbles, carries, recoveries, pressures,
        progressive_passes, preferred_foot.
    """
    name = player.get("player_name", "Unknown")

    # ── Card container ──────────────────────────────────────────────
    with st.container():
        # Header row
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {name}")
        with col2:
            # SPORTA tier badge (rendered via lightweight inline span)
            tier = player.get("sporta_tier", "Low")
            st.markdown(
                f"<span class='sporta-badge {tier.lower()}'>{tier}</span>",
                unsafe_allow_html=True,
            )

        # Meta line (club · nationality · position · age)
        meta_parts = [
            player.get("club") or "—",
            player.get("nationality") or "—",
            player.get("position") or "—",
        ]
        age = player.get("age")
        if age is not None:
            meta_parts.append(f"{age} yrs")
        minutes = player.get("minutes_played")
        if minutes is not None:
            meta_parts.append(f"{int(minutes)} min")
        st.caption(" · ".join(meta_parts))

        # Badges (tier, position, preferred foot)
        render_badges(player)

        st.divider()

        # ── Primary KPIs ────────────────────────────────────────────
        st.markdown("**Primary KPIs**")
        render_metrics(
            {
                "sporta_score": player.get("sporta_score"),
                "similarity": player.get("similarity_pct"),
                "goals": player.get("goals"),
                "total_xg": player.get("total_xg"),
                "assists": player.get("assists"),
                "pass_accuracy": player.get("pass_accuracy"),
            },
            num_columns=6,
        )

        st.divider()

        # ── Secondary KPIs ──────────────────────────────────────────
        st.markdown("**Secondary KPIs**")
        render_metrics(
            {
                "dribbles": player.get("dribbles"),
                "recoveries": player.get("recoveries"),
                "pressures": player.get("pressures"),
                "carries": player.get("carries"),
                "progressive_passes": player.get("progressive_passes"),
                "passes": player.get("passes"),
            },
            num_columns=6,
        )

        st.divider()

        # ── Similarity progress bar ──────────────────────────────────
        st.markdown("**Match Profile**")
        sim_pct = player.get("similarity_pct", 0) or 0
        render_similarity_bar(sim_pct)

        # ── Action buttons ──────────────────────────────────────────
        render_action_buttons(name)

        st.divider()

        with st.expander("🤖 AI Scout Report"):
            report = {
                "strengths": [
                    "Excellent passing",
                    "Strong positioning"
                ],
                "weaknesses": [
                    "Average finishing"
                ],
                "playing_style": "Deep-Lying Playmaker",
                "tactical_suitability": "Excellent fit for possession systems.",
                "development_potential": "High",
                "transfer_risk": "Low",
                "overall_verdict": "Highly recommended replacement."
            }

            st.subheader("💪 Strengths")
            strengths = report.get("strengths", [])
            if strengths:
                for s in strengths:
                    st.markdown(f"• {s}")
            else:
                st.markdown("No strengths identified from available data.")

            st.subheader("⚠️ Weaknesses")
            weaknesses = report.get("weaknesses", [])
            if weaknesses:
                for w in weaknesses:
                    st.markdown(f"• {w}")
            else:
                st.markdown("No major weaknesses identified from available data.")

            st.subheader("🎯 Playing Style")
            st.markdown(report.get("playing_style", "Unavailable"))

            st.subheader("🧠 Tactical Suitability")
            st.markdown(report.get("tactical_suitability", "Unavailable"))

            st.subheader("📈 Development Potential")
            st.markdown(report.get("development_potential", "Unavailable"))

            st.subheader("⚠️ Transfer Risk")
            st.markdown(report.get("transfer_risk", "Unavailable"))

            st.subheader("📋 Overall Verdict")
            st.markdown(report.get("overall_verdict", "AI Scout Report unavailable."))

