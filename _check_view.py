"""Check vw_scouting columns and sample data."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(".").resolve()))

from sqlalchemy import text
from database.db_connection import engine

with engine.connect() as c:
    rows = c.execute(text("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'vw_scouting'
        ORDER BY ordinal_position
    """)).fetchall()
    print("=== vw_scouting columns ===")
    for r in rows:
        print(f"  {r[0]}  ({r[1]})")

    print("\n=== Sample row ===")
    r = c.execute(text("SELECT * FROM vw_scouting LIMIT 1")).fetchone()
    print(r)

    print("\n=== vw_sporta_score columns ===")
    rows = c.execute(text("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'vw_sporta_score'
        ORDER BY ordinal_position
    """).fetchall())
    for r in rows:
        print(f"  {r[0]}  ({r[1]})")

    print("\n=== mv_player_base_stats columns ===")
    rows = c.execute(text("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'mv_player_base_stats'
        ORDER BY ordinal_position
    """).fetchall())
    for r in rows:
        print(f"  {r[0]}  ({r[1]})")
