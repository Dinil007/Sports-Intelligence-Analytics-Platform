"""
database/fix_views.py
=====================
Full rebuild of all SPORTA VISTA PRO views with normalized SPORTA Score (0-100).
Requires minimum 3 matches played to qualify for scoring.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from database.db_connection import engine, text

STATEMENTS = [
    # --- Drop all views in safe dependency order ---
    ("DROP VIEW IF EXISTS vw_scouting     CASCADE", "Drop vw_scouting"),
    ("DROP VIEW IF EXISTS vw_sporta_score CASCADE", "Drop vw_sporta_score"),
    ("DROP VIEW IF EXISTS vw_player_stats CASCADE", "Drop vw_player_stats"),
    ("DROP MATERIALIZED VIEW IF EXISTS mv_player_base_stats CASCADE",
     "Drop mv_player_base_stats"),

    # --- Rebuild materialized view ---
    ("""
    CREATE MATERIALIZED VIEW mv_player_base_stats AS
    SELECT
        player_id,
        player_name,
        COUNT(DISTINCT match_id)                                  AS matches_played,
        COUNT(*)                                                  AS total_events,
        COUNT(*) FILTER (WHERE event_type = 'Pass')              AS passes,
        COUNT(*) FILTER (WHERE event_type = 'Shot')              AS shots,
        COUNT(*) FILTER (WHERE event_type = 'Carry')             AS carries,
        COUNT(*) FILTER (WHERE event_type = 'Pressure')          AS pressures,
        COUNT(*) FILTER (WHERE event_type = 'Ball Recovery')     AS recoveries,
        COUNT(*) FILTER (WHERE event_type = 'Dribble')           AS dribbles
    FROM fact_match_events
    WHERE player_id IS NOT NULL
    GROUP BY player_id, player_name
    """, "Creating mv_player_base_stats (~3-4 min)"),

    ("CREATE INDEX idx_mvpbs_player_id   ON mv_player_base_stats (player_id)",
     "Index: player_id"),
    ("CREATE INDEX idx_mvpbs_player_name ON mv_player_base_stats (player_name)",
     "Index: player_name"),

    # --- vw_player_stats ---
    ("""
    CREATE VIEW vw_player_stats AS
    SELECT player_id, player_name, matches_played, total_events,
           passes, shots, carries, pressures, recoveries, dribbles
    FROM mv_player_base_stats
    """, "Create vw_player_stats"),

    # --- Normalized vw_sporta_score (0-100)
    #     Minimum 3 matches required to qualify (filters out 1-game wonders)
    #     Formula: 40 base + 0.60 * weighted_score
    #       weights: goals 15, xG 10, passes 20, shots 5,
    #                carries 10, pressures 15, recoveries 15, dribbles 10
    ("""
    CREATE VIEW vw_sporta_score AS
    WITH base AS (
        SELECT
            b.player_id, b.player_name, b.matches_played,
            b.passes, b.shots, b.carries, b.pressures,
            b.recoveries, b.dribbles,
            COALESCE(g.goals,    0)   AS goals,
            COALESCE(g.total_xg, 0.0) AS total_xg
        FROM mv_player_base_stats b
        LEFT JOIN vw_top_goal_scorers g ON b.player_name = g.player_name
        WHERE b.matches_played >= 3
    ),
    per_match AS (
        SELECT *,
            passes::numeric    / matches_played AS passes_pm,
            shots::numeric     / matches_played AS shots_pm,
            carries::numeric   / matches_played AS carries_pm,
            pressures::numeric / matches_played AS pressures_pm,
            recoveries::numeric/ matches_played AS recoveries_pm,
            dribbles::numeric  / matches_played AS dribbles_pm,
            goals::numeric     / matches_played AS goals_pm,
            total_xg::numeric  / matches_played AS xg_pm
        FROM base
    ),
    normalized AS (
        SELECT *,
            LEAST(goals_pm       / 0.50, 1.0) AS f_goals,
            LEAST(xg_pm         / 0.40, 1.0) AS f_xg,
            LEAST(passes_pm     / 60.0, 1.0) AS f_passes,
            LEAST(shots_pm      / 4.0,  1.0) AS f_shots,
            LEAST(carries_pm    / 65.0, 1.0) AS f_carries,
            LEAST(pressures_pm  / 15.0, 1.0) AS f_pressures,
            LEAST(recoveries_pm / 5.0,  1.0) AS f_recoveries,
            LEAST(dribbles_pm   / 8.0,  1.0) AS f_dribbles
        FROM per_match
    )
    SELECT
        player_id, player_name, matches_played,
        passes, shots, carries, pressures, recoveries, dribbles,
        goals, total_xg,
        ROUND(
            LEAST(GREATEST(
                40.0 + 0.60 * (
                    15.0 * f_goals      + 10.0 * f_xg         +
                    20.0 * f_passes     +  5.0 * f_shots       +
                    10.0 * f_carries    + 15.0 * f_pressures   +
                    15.0 * f_recoveries + 10.0 * f_dribbles
                ), 0.0), 100.0
            )::numeric, 2
        ) AS sporta_score
    FROM normalized
    """, "Create normalized vw_sporta_score (0-100, min 3 matches)"),

    # --- vw_scouting ---
    ("""
    CREATE VIEW vw_scouting AS
    SELECT player_name, matches_played, sporta_score, goals, total_xg,
           shots, passes, carries, pressures, recoveries, dribbles
    FROM vw_sporta_score
    ORDER BY sporta_score DESC
    """, "Create vw_scouting"),
]


def fix_views():
    print("=" * 58)
    print("  SPORTA VISTA PRO - Full View Rebuild")
    print("=" * 58)
    with engine.connect() as conn:
        for sql, label in STATEMENTS:
            print(f"\n>> {label} ...")
            with conn.begin():
                conn.execute(text(sql))
            print("   Done.")
    print("\n" + "=" * 58)
    print("  All views rebuilt successfully!")
    print("=" * 58)


def verify():
    print("\n>> Top 15 players by SPORTA Score:")
    q = """
    SELECT player_name, matches_played, goals, sporta_score
    FROM vw_sporta_score ORDER BY sporta_score DESC LIMIT 15;
    """
    with engine.connect() as conn:
        rows = conn.execute(text(q)).fetchall()
    print(f"\n{'Player':<38} {'M':>6} {'G':>5} {'Score':>7}  Tier")
    print("-" * 65)
    for r in rows:
        sc = float(r[3])
        tier = ("Elite" if sc>=90 else "Excellent" if sc>=80 else
                "Good"  if sc>=70 else "Average"  if sc>=60 else "Needs Impr.")
        try:
            print(f"{r[0][:38]:<38} {r[1]:>6} {r[2]:>5} {sc:>7.2f}  {tier}")
        except Exception:
            pass


if __name__ == "__main__":
    fix_views()
    verify()
