"""
database/player_repository.py
==============================
Data access layer for player profiles.
All SQL queries related to players live here.
"""

from __future__ import annotations

from sqlalchemy import text

from database.db_connection import engine


# ---------------------------------------------------------------------------
# Profile fetch
# ---------------------------------------------------------------------------

def fetch_player_profile(player_name: str) -> dict:
    """
    Return a raw profile dict for *player_name* by joining:
      dim_players  → nickname, jersey_number, country_name (nationality)
      fact_match_events → most recent team name
      vw_sporta_score   → matches_played, sporta_score + all performance stats

    Fields not available in the DB will be absent from the returned dict
    (handled by the service layer).
    """
    sql = text("""
        WITH latest_team AS (
            -- Pick the team the player appeared for most recently
            SELECT
                player_id::double precision AS player_id,
                player_name,
                team_name
            FROM (
                SELECT
                    player_id,
                    player_name,
                    team_name,
                    ROW_NUMBER() OVER (
                        PARTITION BY player_id
                        ORDER BY match_id DESC
                    ) AS rn
                FROM fact_match_events
                WHERE player_name = :name
                  AND player_id IS NOT NULL
                  AND team_name  IS NOT NULL
            ) sub
            WHERE rn = 1
        )
        SELECT
            dp.player_id,
            dp.player_name,
            dp.nickname,
            dp.jersey_number,
            dp.country_name                              AS nationality,
            lt.team_name,
            s.matches_played,
            s.passes,
            s.shots,
            s.carries,
            s.pressures,
            s.recoveries,
            s.dribbles,
            s.goals,
            s.total_xg,
            s.sporta_score
        FROM dim_players dp
        LEFT JOIN latest_team lt
               ON dp.player_id = lt.player_id
        LEFT JOIN vw_sporta_score s
               ON dp.player_id = s.player_id
        WHERE dp.player_name = :name
        LIMIT 1
    """)

    with engine.connect() as conn:
        row = conn.execute(sql, {"name": player_name}).mappings().first()
        return dict(row) if row else {}


def fetch_player_stats(player_name: str) -> dict:
    """
    Return performance stats from vw_sporta_score for *player_name*.
    Falls back to vw_scouting (which has no player_id) if the join misses.
    """
    sql = text("""
        SELECT
            player_name,
            matches_played,
            passes,
            shots,
            carries,
            pressures,
            recoveries,
            dribbles,
            goals,
            total_xg,
            sporta_score
        FROM vw_sporta_score
        WHERE player_name = :name
        LIMIT 1
    """)
    with engine.connect() as conn:
        row = conn.execute(sql, {"name": player_name}).mappings().first()
        return dict(row) if row else {}


def fetch_player_name_list() -> list[str]:
    """Return all player names available in the scouting view (sorted)."""
    sql = text("SELECT DISTINCT player_name FROM vw_scouting ORDER BY player_name")
    with engine.connect() as conn:
        return [r[0] for r in conn.execute(sql).fetchall()]
