"""
database/recommendation_repository.py
=======================================
Data-access layer for the recommendation engine.
All SQL lives here. No SQL in the UI or service layers.

Responsibilities:
- Fetch player metadata and stats
- Fetch candidate players with optional filters
- Retrieve feature vectors for ML similarity calculations
"""

from __future__ import annotations

from sqlalchemy import text
from database.db_connection import engine

import streamlit as st


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_player(
    player_name: str,
    conn: object | None = None,
) -> dict | None:
    """
    Return full profile for a single player, or None if not found.
    
    Uses existing views:
    - mv_player_base_stats
    - vw_sporta_score
    - fact_match_events (for team inference)
    
    If *conn* is provided, reuse it instead of opening a new one.
    """
    _owns_conn = conn is None
    if _owns_conn:
        conn = engine.connect()
    try:
        # Metadata from dim_players
        meta = conn.execute(
            text("""
                SELECT player_id, player_name, nickname, jersey_number, country_name
                FROM dim_players
                WHERE player_name = :name
                LIMIT 1
            """),
            {"name": player_name},
        ).fetchone()

        if not meta:
            return None

        player_id, player_name, nickname, jersey_number, country_name = meta

        # Primary team from match events (most frequent)
        team_row = conn.execute(
            text("""
                SELECT team_name, COUNT(*) AS cnt
                FROM fact_match_events
                WHERE player_name = :name
                  AND team_name IS NOT NULL
                GROUP BY team_name
                ORDER BY cnt DESC
                LIMIT 1
            """),
            {"name": player_name},
        ).fetchone()

        team_name = team_row[0] if team_row else None

        # Stats from materialized + scoring views
        stats_row = conn.execute(
            text("""
                SELECT
                    b.matches_played,
                    b.shots,
                    COALESCE(b.passes, 0) AS passes,
                    COALESCE(b.carries, 0) AS carries,
                    COALESCE(b.pressures, 0) AS pressures,
                    COALESCE(b.recoveries, 0) AS recoveries,
                    COALESCE(b.dribbles, 0) AS dribbles,
                    COALESCE(s.sporta_score, 0) AS sporta_score,
                    COALESCE(s.goals, 0) AS goals,
                    COALESCE(s.total_xg, 0) AS total_xg
                FROM mv_player_base_stats b
                LEFT JOIN vw_sporta_score s ON b.player_name = s.player_name
                WHERE b.player_name = :name
                LIMIT 1
            """),
            {"name": player_name},
        ).fetchone()

        if not stats_row:
            return {
                "player_id": player_id,
                "player_name": player_name,
                "nickname": nickname,
                "jersey_number": jersey_number,
                "country_name": country_name,
                "team_name": team_name,
                "position": None,
                "age": None,
                "height": None,
                "weight": None,
                "preferred_foot": None,
                "matches_played": None,
                "sporta_score": None,
                "goals": None,
                "total_xg": None,
                "passes": None,
                "shots": None,
                "carries": None,
                "pressures": None,
                "recoveries": None,
                "dribbles": None,
            }

        (
            matches_played,
            passes,
            shots,
            carries,
            pressures,
            recoveries,
            dribbles,
            sporta_score,
            goals,
            total_xg,
        ) = stats_row

        return {
            "player_id": player_id,
            "player_name": player_name,
            "nickname": nickname,
            "jersey_number": jersey_number,
            "country_name": country_name,
            "team_name": team_name,
            "position": None,
            "age": None,
            "height": None,
            "weight": None,
            "preferred_foot": None,
            "matches_played": matches_played,
            "sporta_score": sporta_score,
            "goals": goals,
            "total_xg": total_xg,
            "passes": passes,
            "shots": shots,
            "carries": carries,
            "pressures": pressures,
            "recoveries": recoveries,
            "dribbles": dribbles,
        }
    finally:
        if _owns_conn:
            conn.close()


def get_candidate_players(
    position: str | None = None,
    age_min: int | None = None,
    age_max: int | None = None,
    nationality: str | None = None,
    club: str | None = None,
    competition: str | None = None,
    season: str | None = None,
    budget_tier: str | None = None,
    preferred_foot: str | None = None,
    minutes_played_min: int | None = None,
    minutes_played_max: int | None = None,
    conn: object | None = None,
) -> list[dict]:
    """
    Return candidate players for recommendation, filtered by optional criteria.
    
    Uses existing views:
    - vw_scouting
    - fact_match_events
    - fact_matches
    - dim_competitions
    - dim_seasons
    - dim_players (for nationality)
    
    Filters not yet backed by dataset columns (accepted for API compatibility):
    - position
    - age_min / age_max
    - budget_tier
    - preferred_foot
    
    Filters currently supported:
    - nationality (from dim_players.country_name)
    - club (from fact_match_events.team_name)
    - competition
    - season
    - minutes_played_min / minutes_played_max (using matches_played as proxy)
    """
    # -------------------------------------------------------------------------
    # OPTIMIZED QUERY (was: LEFT JOIN LATERAL ... per-player GROUP BY on the
    # 14.8M-row fact_match_events table -> query never finished).
    #
    # Key change: compute each player's most-frequent team in a SINGLE grouped
    # pass over fact_match_events (one parallel seq scan + hash aggregate) and
    # pick the top team per player with DISTINCT ON, instead of re-running a
    # grouped subquery once per candidate (~6.5k times).
    #
    # Other changes:
    # - Select from vw_sporta_score directly (carries player_id; vw_scouting
    #   drops it and adds a pointless ORDER BY sporta_score DESC).
    # - Select only the columns the recommendation engine actually needs.
    # - No top-level GROUP BY.
    # - club / nationality / minutes / competition / season filters are pushed
    #   into SQL so Python never loads the full player universe to filter it.
    # -------------------------------------------------------------------------
    base_query = """
        SELECT
            s.player_name,
            s.player_id,
            COALESCE(s.sporta_score, 0)   AS sporta_score,
            COALESCE(s.goals, 0)          AS goals,
            COALESCE(s.total_xg, 0)       AS total_xg,
            COALESCE(s.passes, 0)         AS passes,
            COALESCE(s.dribbles, 0)       AS dribbles,
            COALESCE(s.carries, 0)        AS carries,
            COALESCE(s.recoveries, 0)     AS recoveries,
            COALESCE(s.pressures, 0)      AS pressures,
            COALESCE(bt.team_name, 'N/A') AS team_name,
            dp.country_name               AS nationality
        FROM vw_sporta_score s
        LEFT JOIN (
            SELECT DISTINCT ON (player_name) player_name, team_name
            FROM (
                SELECT player_name, team_name, COUNT(*) AS cnt
                FROM fact_match_events
                WHERE team_name IS NOT NULL
                GROUP BY player_name, team_name
            ) tc
            ORDER BY player_name, cnt DESC
        ) bt ON bt.player_name = s.player_name
        LEFT JOIN dim_players dp ON dp.player_name = s.player_name
    """

    conditions = []
    params: dict = {}

    if club:
        conditions.append("bt.team_name = :club")
        params["club"] = club

    if nationality:
        conditions.append("dp.country_name = :nationality")
        params["nationality"] = nationality

    if minutes_played_min is not None:
        conditions.append("s.matches_played >= :minutes_played_min")
        params["minutes_played_min"] = minutes_played_min

    if minutes_played_max is not None:
        conditions.append("s.matches_played <= :minutes_played_max")
        params["minutes_played_max"] = minutes_played_max

    # competition / season: filter to players who appeared in that
    # competition/season via a semi-join against the match dimension tables.
    if competition:
        conditions.append(
            "EXISTS (SELECT 1 FROM fact_match_events fme "
            "JOIN fact_matches fm ON fm.match_id = fme.match_id "
            "JOIN dim_competitions dc ON dc.competition_id = fm.competition_id "
            "WHERE fme.player_name = s.player_name "
            "AND dc.competition_name = :competition)"
        )
        params["competition"] = competition

    if season:
        conditions.append(
            "EXISTS (SELECT 1 FROM fact_match_events fme "
            "JOIN fact_matches fm ON fm.match_id = fme.match_id "
            "JOIN dim_seasons ds ON ds.season_id = fm.season_id "
            "WHERE fme.player_name = s.player_name "
            "AND ds.season_name = :season)"
        )
        params["season"] = season

    # position, age, budget_tier, preferred_foot:
    # accepted for API compatibility but not backed by dataset columns.

    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    base_query += " ORDER BY s.player_name;"

    _owns_conn = conn is None
    if _owns_conn:
        conn = engine.connect()
    try:
        rows = conn.execute(text(base_query), params).fetchall()
    finally:
        if _owns_conn:
            conn.close()

    # Column order from the optimized SELECT:
    # 0 player_name, 1 player_id, 2 sporta_score, 3 goals, 4 total_xg,
    # 5 passes, 6 dribbles, 7 carries, 8 recoveries, 9 pressures,
    # 10 team_name, 11 nationality
    results = []
    for row in rows:
        team = row[10]
        results.append({
            "player_name": row[0],
            "player_id": row[1],
            "team_name": team,
            "club": team,
            "competition_name": None,
            "matches_played": None,
            "minutes_played": None,
            "sporta_score": row[2],
            "goals": row[3],
            "total_xg": row[4],
            "assists": None,
            "pass_accuracy": None,
            "passes": row[5],
            "dribbles": row[6],
            "carries": row[7],
            "recoveries": row[8],
            "pressures": row[9],
            "progressive_passes": None,
            "nationality": row[11],
            "position": None,
            "age": None,
            "preferred_foot": None,
        })

    return results


def get_player_vector(
    player_name: str,
    conn: object | None = None,
    player: dict | None = None,
) -> dict | None:
    """
    Return feature vector for ML similarity calculation.
    
    Returns None if player not found.
    Missing stats are defaulted to 0.0 so the vector is always usable.
    Used by the ML engine to compute cosine similarity.
    
    If *conn* is provided, reuse it when fetching the player record.
    If *player* is provided, skip the database fetch entirely.
    """
    if player is None:
        player = get_player(player_name, conn=conn)
    if not player:
        return None

    required_fields = [
        "sporta_score", "goals", "total_xg",
        "passes", "dribbles", "carries", "recoveries", "pressures"
    ]

    vector = {}
    for field in required_fields:
        value = player.get(field)
        vector[field] = float(value) if value is not None else 0.0

    vector["player_name"] = player_name
    vector["team_name"] = player.get("team_name")
    vector["competition_name"] = None  # Not directly available at player level

    return vector

# ---------------------------------------------------------------------------
# Lightweight filter lookups (cached for UI performance)
# ---------------------------------------------------------------------------

@st.cache_data(ttl=600)
def fetch_candidate_player_names() -> list[str]:
    """Return distinct player names for UI dropdowns."""
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT DISTINCT player_name
                FROM vw_scouting
                ORDER BY player_name
            """)
        ).fetchall()
    return [row[0] for row in rows]


@st.cache_data(ttl=600)
def fetch_candidate_teams() -> list[str]:
    """Return distinct team names for UI dropdowns."""
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT DISTINCT team_name
                FROM dim_teams
                ORDER BY team_name
            """)
        ).fetchall()
    return [row[0] for row in rows]


@st.cache_data(ttl=600)
def fetch_candidate_competitions() -> list[str]:
    """Return competition names for UI dropdowns."""
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT competition_name
                FROM dim_competitions
                ORDER BY competition_name
            """)
        ).fetchall()
    return [row[0] for row in rows]


@st.cache_data(ttl=600)
def fetch_candidate_seasons() -> list[str]:
    """Return season names for UI dropdowns."""
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT season_name
                FROM dim_seasons
                ORDER BY season_name
            """)
        ).fetchall()
    return [row[0] for row in rows]
