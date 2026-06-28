"""Side-by-side recommendation comparison component.

Displays a comparison table between the selected player (reference)
and a recommended player using native Streamlit widgets.
No HTML, no CSS, no pandas required.
"""

from __future__ import annotations

from typing import Any

import streamlit as st


def render_recommendation_comparison(
    selected_player: dict[str, Any],
    recommended_player: dict[str, Any],
) -> None:
    """
    Render a comparison table between the selected player and a recommended player.

    Parameters
    ----------
    selected_player : dict[str, Any]
        The player selected from the filter/search.
    recommended_player : dict[str, Any]
        The recommended player to compare against.
    """
    st.success("Comparison component reached")
    st.write("selected_player:", selected_player)
    st.write("recommended_player:", recommended_player)
    st.subheader("Side-by-Side Comparison")

    rows = [
        ("SPORTA Score", selected_player.get("sporta_score"), recommended_player.get("sporta_score")),
        ("Recommendation Score", selected_player.get("recommendation_score"), recommended_player.get("recommendation_score")),
        ("Similarity %", selected_player.get("similarity_pct"), recommended_player.get("similarity_pct")),
        ("Goals", selected_player.get("goals"), recommended_player.get("goals")),
        ("Assists", selected_player.get("assists"), recommended_player.get("assists")),
        ("xG", selected_player.get("total_xg"), recommended_player.get("total_xg")),
        ("Pass Accuracy", selected_player.get("pass_accuracy"), recommended_player.get("pass_accuracy")),
        ("Passes", selected_player.get("passes"), recommended_player.get("passes")),
        ("Dribbles", selected_player.get("dribbles"), recommended_player.get("dribbles")),
        ("Carries", selected_player.get("carries"), recommended_player.get("carries")),
        ("Recoveries", selected_player.get("recoveries"), recommended_player.get("recoveries")),
        ("Pressures", selected_player.get("pressures"), recommended_player.get("pressures")),
        ("Minutes Played", selected_player.get("minutes_played"), recommended_player.get("minutes_played")),
    ]

    data = [
        {
            "Metric": metric,
            "Selected": selected_val,
            "Recommended": recommended_val,
        }
        for metric, selected_val, recommended_val in rows
    ]

    st.dataframe(data, use_container_width=True, hide_index=True)
