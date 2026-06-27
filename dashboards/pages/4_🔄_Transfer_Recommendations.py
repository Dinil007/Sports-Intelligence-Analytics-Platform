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

from services.recommendation_service import recommend_similar_players
from database.recommendation_repository import (
    fetch_candidate_player_names,
    fetch_candidate_teams,
    fetch_candidate_competitions,
    fetch_candidate_seasons,
)
from dashboards.components.recommendation_card import render_recommendation_card

st.title("🔄 AI Transfer Recommendations")

# Lightweight pre-cached lookups for filter population.
player_names = fetch_candidate_player_names()
teams = fetch_candidate_teams()
competitions = fetch_candidate_competitions()
seasons = fetch_candidate_seasons()

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
    recommendations = recommend_similar_players(
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

    if not recommendations:
        st.info("No recommendations available for the selected player with the current filters.")
    else:
        st.subheader("Recommended Players")
        # Inject badge CSS once before rendering cards
        # st.markdown(get_card_css(), unsafe_allow_html=True)

        for rec in recommendations:
            render_recommendation_card(rec)


