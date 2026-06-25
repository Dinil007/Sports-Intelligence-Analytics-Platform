"""
database/recreate_views.py
===========================
Authoritative script to rebuild all SPORTA VISTA PRO database views.
Run this ONCE to migrate to the normalized (0–100) SPORTA Score.

Usage:
    python database/recreate_views.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from database.db_connection import engine, text

# ---------------------------------------------------------------------------
# SQL Statements (ordered by dependency)
# ---------------------------------------------------------------------------

STATEMENTS = [
    # ------------------------------------------------------------------
    # 1. Materialized view: one fast full-table scan gives us all per-player
    #    stats INCLUDING matches_played. This avoids re-scanning 14.8M rows
    #    on every dashboard query.
    # ------------------------------------------------------------------
    (
        "DROP MATERIALIZED VIEW IF EXISTS mv_player_base_stats CASCADE",
        "Dropping old materialized view (if any)"
    ),
    (
        """
        CREATE MATERIALIZED VIEW mv_player_base_stats AS
        SELECT
            player_id,
            player_name,
            COUNT(DISTINCT match_id)                                        AS matches_played,
            COUNT(*)                                                        AS total_events,
            COUNT(*) FILTER (WHERE event_type = 'Pass')                    AS passes,
            COUNT(*) FILTER (WHERE event_type = 'Shot')                    AS shots,
            COUNT(*) FILTER (WHERE event_type = 'Carry')                   AS carries,
            COUNT(*) FILTER (WHERE event_type = 'Pressure')                AS pressures,
            COUNT(*) FILTER (WHERE event_type = 'Ball Recovery')           AS recoveries,
            COUNT(*) FILTER (WHERE event_type = 'Dribble')                 AS dribbles
        FROM fact_match_events
        WHERE player_id IS NOT NULL
        GROUP BY player_id, player_name
        """,
        "Creating mv_player_base_stats"
    ),
    (
        "CREATE INDEX idx_mv_player_base_player_id   ON mv_player_base_stats (player_id)",
        "Indexing mv_player_base_stats.player_id"
    ),
    (
        "CREATE INDEX idx_mv_player_base_player_name ON mv_player_base_stats (player_name)",
        "Indexing mv_player_base_stats.player_name"
    ),

    # ------------------------------------------------------------------
    # 2. vw_player_stats — now backed by the materialized view so it
    #    includes matches_played without re-aggregating events.
    #    Must DROP first because CREATE OR REPLACE cannot reorder columns.
    # ------------------------------------------------------------------
    (
        "DROP VIEW IF EXISTS vw_player_stats CASCADE",
        "Dropping old vw_player_stats"
    ),
    (
        """
        CREATE VIEW vw_player_stats AS
        SELECT
            player_id,
            player_name,
            matches_played,
            total_events,
            passes,
            shots,
            carries,
            pressures,
            recoveries,
            dribbles
        FROM mv_player_base_stats
        """,
        "Creating new vw_player_stats with matches_played"
    ),

    # ------------------------------------------------------------------
    # 3. vw_sporta_score — NORMALIZED 0–100 formula
    #
    #    Per-match caps (= elite benchmark → factor of 1.0):
    #      goals       0.50 / match
    #      xG          0.40 / match
    #      passes     60    / match
    #      shots       4    / match
    #      carries    65    / match
    #      pressures  15    / match
    #      recoveries  5    / match
    #      dribbles    8    / match
    #
    #    Weights (sum = 100):
    #      goals 15 · xG 10 · passes 20 · shots 5
    #      carries 10 · pressures 15 · recoveries 15 · dribbles 10
    #
    #    Final:  sporta_score = 40 + 0.60 * weighted_score   ∈ [40, 100]
    #    (Active players start at ≥ 40; elite performers reach ~92–96)
    # ------------------------------------------------------------------
    (
        """
        CREATE OR REPLACE VIEW vw_sporta_score AS
        WITH base AS (
            SELECT
                b.player_id,
                b.player_name,
                b.matches_played,
                b.passes,
                b.shots,
                b.carries,
                b.pressures,
                b.recoveries,
                b.dribbles,
                COALESCE(g.goals,    0)   AS goals,
                COALESCE(g.total_xg, 0.0) AS total_xg
            FROM mv_player_base_stats b
            LEFT JOIN vw_top_goal_scorers g ON b.player_name = g.player_name
        ),
        per_match AS (
            SELECT *,
                CASE WHEN matches_played > 0 THEN passes::numeric    / matches_played ELSE 0 END AS passes_pm,
                CASE WHEN matches_played > 0 THEN shots::numeric     / matches_played ELSE 0 END AS shots_pm,
                CASE WHEN matches_played > 0 THEN carries::numeric   / matches_played ELSE 0 END AS carries_pm,
                CASE WHEN matches_played > 0 THEN pressures::numeric / matches_played ELSE 0 END AS pressures_pm,
                CASE WHEN matches_played > 0 THEN recoveries::numeric/ matches_played ELSE 0 END AS recoveries_pm,
                CASE WHEN matches_played > 0 THEN dribbles::numeric  / matches_played ELSE 0 END AS dribbles_pm,
                CASE WHEN matches_played > 0 THEN goals::numeric     / matches_played ELSE 0 END AS goals_pm,
                CASE WHEN matches_played > 0 THEN total_xg::numeric  / matches_played ELSE 0 END AS xg_pm
            FROM base
        ),
        normalized AS (
            SELECT *,
                LEAST(goals_pm      / 0.50, 1.0) AS f_goals,
                LEAST(xg_pm        / 0.40, 1.0) AS f_xg,
                LEAST(passes_pm    / 60.0, 1.0) AS f_passes,
                LEAST(shots_pm     / 4.0,  1.0) AS f_shots,
                LEAST(carries_pm   / 65.0, 1.0) AS f_carries,
                LEAST(pressures_pm / 15.0, 1.0) AS f_pressures,
                LEAST(recoveries_pm/ 5.0,  1.0) AS f_recoveries,
                LEAST(dribbles_pm  / 8.0,  1.0) AS f_dribbles
            FROM per_match
        )
        SELECT
            player_id,
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
            ROUND(
                LEAST(
                    GREATEST(
                        40.0 + 0.60 * (
                            15.0 * f_goals     +
                            10.0 * f_xg        +
                            20.0 * f_passes    +
                             5.0 * f_shots     +
                            10.0 * f_carries   +
                            15.0 * f_pressures +
                            15.0 * f_recoveries+
                            10.0 * f_dribbles
                        ),
                        0.0
                    ),
                    100.0
                )::numeric,
                2
            ) AS sporta_score
        FROM normalized
        """,
        "Recreating vw_sporta_score with normalized formula"
    ),

    # ------------------------------------------------------------------
    # 4. vw_scouting — expose all useful columns from the new score view
    # ------------------------------------------------------------------
    (
        """
        CREATE OR REPLACE VIEW vw_scouting AS
        SELECT
            player_name,
            matches_played,
            sporta_score,
            goals,
            total_xg,
            shots,
            passes,
            carries,
            pressures,
            recoveries,
            dribbles
        FROM vw_sporta_score
        ORDER BY sporta_score DESC
        """,
        "Recreating vw_scouting"
    ),
]

# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def recreate_views():
    print("=" * 60)
    print("  SPORTA VISTA PRO - Rebuilding Database Views")
    print("=" * 60)

    with engine.connect() as conn:
        with conn.begin():
            for sql, label in STATEMENTS:
                print(f"\n>> {label} ...")
                conn.execute(text(sql))
                print(f"   Done.")

    print("\n" + "=" * 60)
    print("  All views rebuilt successfully.")
    print("=" * 60)


def verify_scores():
    """Quick sanity check - print top 10 players after rebuild."""
    print("\n>> Verifying top 10 SPORTA Scores ...")
    query = """
    SELECT player_name, matches_played, goals, sporta_score
    FROM vw_sporta_score
    ORDER BY sporta_score DESC
    LIMIT 10;
    """
    with engine.connect() as conn:
        rows = conn.execute(text(query)).fetchall()
        print(f"\n{'Player':<35} {'Matches':>7} {'Goals':>6} {'Score':>7}")
        print("-" * 60)
        for r in rows:
            print(f"{r[1]:<35} {r[2]:>7} {r[3]:>6} {float(r[4]):>7.2f}")


if __name__ == "__main__":
    recreate_views()
    verify_scores()
