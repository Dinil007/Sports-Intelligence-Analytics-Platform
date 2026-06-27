"""
database/player_repository.py
==============================
Data-access layer for player profile and statistics.
All SQL lives here. No SQL in the UI or service layers.

Available data sources:
  - dim_players  : player_id, player_name, nickname, jersey_number, country_name  (11,889 rows)
  - dim_teams    : team_id, team_name  (354 rows)
  - fact_match_events : team_name per event  (indexed on player_name)
  - mv_player_base_stats : matches_played + event counts  (materialized, fast)
  - vw_sporta_score      : normalized 0-100 score + goals + xg
  - vw_top_goal_scorers  : goals, total_xg

NOTE: position, age, height, weight, preferred_foot are NOT in the StatsBomb dataset.
      These will be returned as None and displayed as "N/A" by the service layer.
"""

from __future__ import annotations
from sqlalchemy import text
from database.db_connection import engine


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def fetch_player_profile(player_name: str) -> dict:
    """
    Return a raw dict with all available metadata + stats for *player_name*.
    Missing fields are explicitly set to None — the service layer handles defaults.
    """
    profile: dict = {
        # Identity / metadata
        "player_id":     None,
        "player_name":   player_name,
        "nickname":      None,
        "jersey_number": None,
        "country_name":  None,
        "team_name":     None,
        # Not stored in StatsBomb data
        "position":      None,
        "age":           None,
        "height":        None,
        "weight":        None,
        "preferred_foot": None,
        # Performance
        "matches_played": None,
        "sporta_score":   None,
        "goals":          None,
        "total_xg":       None,
        "passes":         None,
        "shots":          None,
        "carries":        None,
        "pressures":      None,
        "recoveries":     None,
        "dribbles":       None,
    }

    with engine.connect() as conn:
        # --- 1. Metadata from dim_players ---
        meta = conn.execute(
            text("""
                SELECT player_id, player_name, nickname, jersey_number, country_name
                FROM dim_players
                WHERE player_name = :name
                LIMIT 1
            """),
            {"name": player_name},
        ).fetchone()

        if meta:
            profile["player_id"]     = meta[0]
            profile["player_name"]   = meta[1]
            profile["nickname"]      = meta[2]
            profile["jersey_number"] = meta[3]
            profile["country_name"]  = meta[4]

        # --- 2. Primary team from fact_match_events (uses player_name index) ---
        # We pick the team the player appeared for most often.
        team_row = conn.execute(
            text("""
                SELECT team_name, COUNT(*) AS cnt
                FROM fact_match_events
                WHERE player_name = :name
                  AND team_name   IS NOT NULL
                GROUP BY team_name
                ORDER BY cnt DESC
                LIMIT 1
            """),
            {"name": player_name},
        ).fetchone()

        if team_row:
            profile["team_name"] = team_row[0]

        # --- 3. Aggregated stats from materialized view + scoring view ---
        stats_row = conn.execute(
            text("""
                SELECT
                    b.matches_played,
                    b.passes,
                    b.shots,
                    b.carries,
                    b.pressures,
                    b.recoveries,
                    b.dribbles,
                    COALESCE(s.sporta_score, 0) AS sporta_score,
                    COALESCE(s.goals,    0)     AS goals,
                    COALESCE(s.total_xg, 0)     AS total_xg
                FROM mv_player_base_stats b
                LEFT JOIN vw_sporta_score s ON b.player_name = s.player_name
                WHERE b.player_name = :name
                LIMIT 1
            """),
            {"name": player_name},
        ).fetchone()

        if stats_row:
            (
                profile["matches_played"],
                profile["passes"],
                profile["shots"],
                profile["carries"],
                profile["pressures"],
                profile["recoveries"],
                profile["dribbles"],
                profile["sporta_score"],
                profile["goals"],
                profile["total_xg"],
            ) = stats_row

    return profile


def fetch_all_scouting_player_names() -> list[str]:
    """
    Return all player names from vw_scouting (qualified players only, ≥3 matches).
    Used to populate the selectbox.
    """
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT DISTINCT player_name FROM vw_scouting ORDER BY player_name;")
        ).fetchall()
    return [r[0] for r in rows]


def fetch_filtered_player_names(
    competition: str | None = None,
    club: str | None = None,
    season: str | None = None,
    position: str | None = None,
    age_min: int | None = None,
    age_max: int | None = None,
) -> list[str]:
    """
    Return player names filtered by any combination of the supported filters.

    Only filters that are not None are applied; None filters are ignored so
    the function never fails simply because a filter was omitted.

    Parameters:
    -----------
    competition : str, optional
        Competition name to filter by (e.g., "Premier League").
    club : str, optional
        Club / team name to filter by (e.g., "Manchester City").
    season : str, optional
        Season name to filter by (e.g., "2015/2016"). Matched against
        ``dim_seasons.season_name`` via ``fact_matches.season_id``.
    position : str, optional
        Player position to filter by. **Note:** position data is NOT present
        in the StatsBomb dataset, so this filter is accepted for API
        forward-compatibility but currently has no effect.
    age_min : int, optional
        Minimum player age to filter by. **Note:** age data is NOT present
        in the StatsBomb dataset, so this filter is accepted for API
        forward-compatibility but currently has no effect.
    age_max : int, optional
        Maximum player age to filter by. **Note:** age data is NOT present
        in the StatsBomb dataset, so this filter is accepted for API
        forward-compatibility but currently has no effect.

    Returns:
    --------
    list[str]
        Filtered list of player names from ``vw_scouting``.
    """
    # Build dynamic query with optional filters.
    # Joins:
    #   vw_scouting -> fact_match_events (player_name)
    #   fact_match_events -> fact_matches (match_id)
    #   fact_matches -> dim_competitions (competition_id)
    #   fact_matches -> dim_seasons (season_id)
    query = """
        SELECT DISTINCT s.player_name
        FROM vw_scouting s
        INNER JOIN fact_match_events fme ON s.player_name = fme.player_name
        INNER JOIN fact_matches fm ON fme.match_id = fm.match_id
        INNER JOIN dim_competitions dc ON fm.competition_id = dc.competition_id
        INNER JOIN dim_seasons ds ON fm.season_id = ds.season_id
    """

    conditions = []
    params: dict = {}

    if competition:
        conditions.append("dc.competition_name = :competition")
        params["competition"] = competition

    if club:
        conditions.append("fme.team_name = :club")
        params["club"] = club

    if season:
        conditions.append("ds.season_name = :season")
        params["season"] = season

    # position / age: accepted for API compatibility but not yet backed by
    # database columns. When the data becomes available, add the relevant
    # conditions here (e.g. on dim_players.position / dim_players.age).
    # They are intentionally NOT applied today so callers can pass them
    # without causing failures.
    if position:
        pass
    if age_min is not None or age_max is not None:
        pass

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY s.player_name;"

    with engine.connect() as conn:
        rows = conn.execute(text(query), params).fetchall()
    return [r[0] for r in rows]


def fetch_all_competitions() -> list[str]:
    """
    Return all competition names from dim_competitions.
    Used to populate the competition filter dropdown.
    """
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT DISTINCT competition_name FROM dim_competitions ORDER BY competition_name;")
        ).fetchall()
    return [r[0] for r in rows]


def fetch_all_teams() -> list[str]:
    """
    Return all team names from dim_teams.
    Used to populate the team filter dropdown.
    """
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT DISTINCT team_name FROM dim_teams ORDER BY team_name;")
        ).fetchall()
    return [r[0] for r in rows]


def fetch_all_seasons() -> list[str]:
    """
    Return all season names from dim_seasons.
    Used to populate the season filter dropdown.
    """
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT DISTINCT season_name FROM dim_seasons ORDER BY season_name;")
        ).fetchall()
    return [r[0] for r in rows]
