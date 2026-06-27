"""Run EXPLAIN ANALYZE on the new query, then run the full query with cursor iteration."""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(".").resolve()))

from sqlalchemy import text
from database.db_connection import engine

new_query = """
    SELECT
        s.player_name,
        COALESCE(s.team_name, 'N/A') AS team_name,
        'N/A' AS competition_name,
        b.matches_played,
        COALESCE(sc.sporta_score, 0) AS sporta_score,
        COALESCE(sc.goals, 0) AS goals,
        COALESCE(sc.total_xg, 0) AS total_xg,
        COALESCE(b.passes, 0) AS passes,
        COALESCE(b.dribbles, 0) AS dribbles,
        COALESCE(b.carries, 0) AS carries,
        COALESCE(b.recoveries, 0) AS recoveries,
        COALESCE(b.pressures, 0) AS pressures,
        dp.country_name
    FROM vw_scouting s
    LEFT JOIN mv_player_base_stats b ON s.player_name = b.player_name
    LEFT JOIN vw_sporta_score sc ON s.player_name = sc.player_name
    LEFT JOIN dim_players dp ON s.player_name = dp.player_name
    GROUP BY s.player_name, s.team_name, b.matches_played,
             sc.sporta_score, sc.goals, sc.total_xg,
             b.passes, b.dribbles, b.carries, b.recoveries, b.pressures,
             dp.country_name
    ORDER BY s.player_name
    LIMIT 10;
"""

print("=== EXPLAIN ANALYZE (new query, LIMIT 10) ===")
try:
    with engine.connect() as c:
        rows = c.execute(text("EXPLAIN ANALYZE " + new_query)).fetchall()
        for row in rows:
            print(f"  {row[0]}")
except Exception as e:
    print(f"EXPLAIN ANALYZE ERROR: {e}")

print("\n=== Full query (fetch all), timed ===")
try:
    full_q = new_query.replace("LIMIT 10", "")
    t0 = time.perf_counter()
    with engine.connect() as c:
        rows = c.execute(text(full_q)).fetchall()
        dt = time.perf_counter() - t0
        print(f"Returned {len(rows)} rows in {dt:.2f}s")
        if rows:
            print(f"First row: player_name={rows[0][0]}, sporta={rows[0][4]}")
except Exception as e:
    print(f"QUERY ERROR: {e}")

print("\n=== vw_scouting row count ===")
try:
    with engine.connect() as c:
        r = c.execute(text("SELECT COUNT(*) FROM vw_scouting")).scalar()
        print(f"  vw_scouting: {r}")
        r = c.execute(text("SELECT COUNT(*) FROM mv_player_base_stats")).scalar()
        print(f"  mv_player_base_stats: {r}")
        r = c.execute(text("SELECT COUNT(*) FROM vw_sporta_score")).scalar()
        print(f"  vw_sporta_score: {r}")
except Exception as e:
    print(f"COUNT ERROR: {e}")
