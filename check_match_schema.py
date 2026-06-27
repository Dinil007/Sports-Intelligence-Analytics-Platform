#!/usr/bin/env python3
"""Check match-related table schemas."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from database.db_connection import engine, text

print("=" * 60)
print("CHECKING MATCH-RELATED TABLES")
print("=" * 60)

with engine.connect() as conn:
    # Check fact_matches columns
    print("\nfact_matches columns:")
    result = conn.execute(text("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'fact_matches' 
        ORDER BY ordinal_position;
    """))
    for col_name, col_type in result.fetchall():
        print(f"  - {col_name} ({col_type})")
    
    # Check matches columns
    print("\nmatches columns:")
    result = conn.execute(text("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'matches' 
        ORDER BY ordinal_position;
    """))
    for col_name, col_type in result.fetchall():
        print(f"  - {col_name} ({col_type})")
    
    # Check a sample from fact_matches
    print("\nSample fact_matches row:")
    result = conn.execute(text("SELECT * FROM fact_matches LIMIT 1"))
    row = result.fetchone()
    if row:
        cols = [desc[0] for desc in result.description]
        for col, val in zip(cols, row):
            print(f"  {col}: {val}")
    
    # Check how to link match_id to competition
    print("\nChecking match_id linkage:")
    result = conn.execute(text("""
        SELECT DISTINCT fme.match_id, fm.competition_name
        FROM fact_match_events fme
        LEFT JOIN fact_matches fm ON fme.match_id = fm.match_id
        WHERE fme.match_id IS NOT NULL
        LIMIT 5;
    """))
    for row in result.fetchall():
        print(f"  match_id: {row[0]}, competition: {row[1]}")

print("\n" + "=" * 60)
print("Check complete!")
print("=" * 60)