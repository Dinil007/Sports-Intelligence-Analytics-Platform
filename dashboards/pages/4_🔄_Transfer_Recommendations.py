import sys
from pathlib import Path

# Ensure project root is importable when running as a Streamlit page.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import streamlit as st

from auth.streamlit_auth import is_authenticated

if not is_authenticated():
    st.stop()

from services.recommendation_service import (
    recommend_similar_players,
    get_selected_player,
    fetch_candidate_player_names,
    fetch_candidate_teams,
    fetch_candidate_competitions,
    fetch_candidate_seasons,
)
from services.transfer_advisor_service import generate_transfer_advisor
from dashboards.components.recommendation_card import render_recommendation_card
from dashboards.components.recommendation_categories import (
    render_recommendation_categories,
)
from dashboards.components.recommendation_comparison import (
    render_recommendation_comparison,
)
from dashboards.components.recommendation_summary import render_recommendation_summary
from dashboards.components.transfer_advisor import render_transfer_advisor
from dashboards.components.visualizations.recommendation_dashboard import (
    render_recommendation_dashboard,
)

st.title("🔄 AI Transfer Recommendations")

# Lightweight pre-cached lookups for filter population.
player_names = fetch_candidate_player_names()
teams = fetch_candidate_teams()
competitions = fetch_candidate_competitions()
seasons = fetch_candidate_seasons()


# Initialize session state for recommendations persistence across reruns.
if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

if "selected_player_name" not in st.session_state:
    st.session_state.selected_player_name = None

if "has_searched" not in st.session_state:
    st.session_state.has_searched = False

if "compare_player" not in st.session_state:
    st.session_state.compare_player = None

with st.container():
    st.header("Refine Recommendations")

    selected_player = st.selectbox(
        "Choose a player",
        player_names,
        key="player_select",
    )

    club = st.selectbox(
        "🏟️ Club",
        [""] + teams,
        key="club_filter",
    ) or None

    competition = st.selectbox(
        "🏆 Competition",
        [""] + competitions,
        key="competition_filter",
    ) or None

    season = st.selectbox(
        "📅 Season",
        [""] + seasons,
        key="season_filter",
    ) or None

    # Accepted but not yet enforced by the dataset (forward-compatible placeholders).
    position = st.selectbox(
        "📍 Position",
        ["", "Goalkeeper", "Defender", "Midfielder", "Forward"],
        key="position_filter",
    ) or None

    age_min, age_max = st.select_slider(
        "🎂 Age Range",
        options=list(range(16, 46)),
        value=(16, 45),
        key="age_filter",
    )
    # Convert to None when the full range is selected so the filter is effectively disabled.
    age_min = None if age_min == 16 else age_min
    age_max = None if age_max == 45 else age_max

    budget_tier = st.selectbox(
        "💰 Budget Tier",
        ["", "Low", "Medium", "High", "Elite"],
        key="budget_filter",
    ) or None

    preferred_foot = st.selectbox(
        "⚽ Preferred Foot",
        ["", "Left", "Right", "Both"],
        key="foot_filter",
    ) or None

    minutes_played_min = st.number_input(
        "⏱️ Minutes Played (min)",
        min_value=0,
        value=0,
        step=90,
        key="min_minutes_filter",
    )
    minutes_played_min = minutes_played_min if minutes_played_min > 0 else None

if st.button("Find Similar Players", use_container_width=True):
    st.session_state.recommendations = recommend_similar_players(
        selected_player,
        position=position,
        age_min=age_min,
        age_max=age_max,
        nationality=None,
        club=club,
        competition=competition,
        season=season,
        budget_tier=budget_tier,
        preferred_foot=preferred_foot,
        minutes_played_min=minutes_played_min,
    )

    st.session_state.selected_player_name = selected_player
    st.session_state.has_searched = True
    st.session_state.pop("compare_player", None)

if st.session_state.has_searched:
    if not st.session_state.recommendations:
        st.info("No recommendations available.")
    else:
        render_recommendation_summary(
            st.session_state.recommendations,
            st.session_state.selected_player_name,
        )

        advisor = generate_transfer_advisor(
            get_selected_player(st.session_state.selected_player_name) or {},
            st.session_state.recommendations,
        )
        render_transfer_advisor(advisor)

        render_recommendation_dashboard(
            st.session_state.recommendations
        )

        st.subheader("Recommended Players")
        # Inject badge CSS once before rendering cards
        # st.markdown(get_card_css(), unsafe_allow_html=True)

        selected_player_dict = get_selected_player(st.session_state.selected_player_name)
        player_options = {
            r.get("player_name", "Unknown"): (index, r)
            for index, r in enumerate(st.session_state.recommendations)
        }

        compare_player = st.session_state.get("compare_player")
        compare_with = st.selectbox(
            "Compare with...",
            [""] + list(player_options.keys()),
            index=list(player_options.keys()).index(compare_player) + 1
            if compare_player and compare_player in player_options
            else 0,
        )
        st.session_state["compare_player"] = compare_with if compare_with else compare_player

        for index, rec in enumerate(st.session_state.recommendations):
            render_recommendation_card(rec, index=index)

        compare_player = st.session_state.get("compare_player")

        if compare_player and compare_player in player_options:
            comparison_index, recommended_player = player_options[compare_player]

            render_recommendation_comparison(
                selected_player_dict or {},
                recommended_player,
                comparison_index=comparison_index,
            )


