"""
dashboards/components/player_strength_comparison.py
===================================================
Executive strength and weakness comparison between two players.

No AI. No repository imports. No SQL.
Uses only metrics supplied in the player dicts.
"""

from __future__ import annotations

from typing import Any

import streamlit as st


def _n(v: Any) -> float:
    try:
        return float(v) if v is not None else 0.0
    except (TypeError, ValueError):
        return 0.0


def _score(player: dict[str, Any]) -> dict[str, float]:
    return {
        "Passing": _n(player.get("pass_accuracy")),
        "Defending": _n(player.get("pressures")) + _n(player.get("recoveries")),
        "Creativity": _n(player.get("dribbles")) + _n(player.get("carries")),
        "Pressing": _n(player.get("pressures")),
        "Ball Progression": _n(player.get("progressive_passes") or player.get("passes")),
        "Finishing": _n(player.get("goals")) + _n(player.get("total_xg")),
        "Aerial Ability": 0.0,
        "Physical Presence": 0.0,
    }


def render_strength_comparison(
    selected_player: dict[str, Any],
    recommended_player: dict[str, Any],
) -> None:
    """
    Render executive strength and weakness sections.

    Parameters
    ----------
    selected_player : dict[str, Any]
    recommended_player : dict[str, Any]
    """
    sel = _score(selected_player)
    rec = _score(recommended_player)

    strengths = ["Passing", "Defending", "Creativity", "Pressing", "Ball Progression"]
    weaknesses = ["Finishing", "Aerial Ability", "Physical Presence"]

    st.markdown("### Strength Comparison")
    for attr in strengths:
        sv = sel.get(attr, 0.0)
        rv = rec.get(attr, 0.0)
        if sv >= rv:
            st.markdown(f"✓ **{attr}** — Selected ({sv:.1f} vs {rv:.1f})")
        else:
            st.markdown(f"✓ **{attr}** — Recommended ({rv:.1f} vs {sv:.1f})")

    st.markdown("### Weakness Comparison")
    for attr in weaknesses:
        sv = sel.get(attr, 0.0)
        rv = rec.get(attr, 0.0)
        if sv <= rv:
            st.markdown(f"• **{attr}** — Selected weaker ({sv:.1f} vs {rv:.1f})")
        else:
            st.markdown(f"• **{attr}** — Recommended weaker ({rv:.1f} vs {sv:.1f})")
