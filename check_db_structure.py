#!/usr/bin/env python3
"""Check database tables and columns available for filtering."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from database.db_connection import engine, text

print("=" * 60)
print("DATABASE TABLES")
print("=" * 60)

with engine.connect() as conn:
    # List all tables
    result = conn.execute(text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name;
    """))
    tables = [r[0] for r in result.fetchall()]
    print("\nTables:")
    for table in tables:
        print(f"  - {table}")
    
    # Check columns for key tables
    print("\n" + "=" * 60)
    print("TABLE COLUMNS")
    print("=" * 60)
    
    key_tables = ['dim_players', 'dim_teams', 'dim_competitions', 'seasons', 
                  'fact_match_events', 'vw_scouting', 'vw_sporta_score']
    
    for table in key_tables:
        if table in tables:
            print(f"\n{table}:")
            result = conn.execute(text(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{table}' 
                ORDER BY ordinal_position;
            """))
            columns = result.fetchall()
            for col_name, col_type in columns:
                print(f"  - {col_name} ({col_type})")
    
    # Check for position, age, club data
    print("\n" + "=" * 60)
    print("FILTER DATA AVAILABILITY")
    print("=" * 60)
    
    # Check if position exists
    result = conn.execute(text("""
        SELECT COUNT(*) as cnt 
        FROM information_schema.columns 
        WHERE table_name = 'dim_players' 
        AND column_name = 'position';
    """))
    has_position = result.fetchone()[0] > 0
    print(f"\nPosition data available: {has_position}")
    
    # Check if age exists
    result = conn.execute(text("""
        SELECT COUNT(*) as cnt 
        FROM information_schema.columns 
        WHERE table_name = 'dim_players' 
        AND column_name = 'age';
    """))
    has_age = result.fetchone()[0] > 0
    print(f"Age data available: {has_age}")
    
    # Check competitions
    print("\nSample competitions:")
    result = conn.execute(text("""
        SELECT DISTINCT competition_name 
        FROM dim_competitions 
        ORDER BY competition_name 
        LIMIT 10;
    """))
    for row in result.fetchall():
        print(f"  - {row[0]}")
    
    # Check seasons from correct table
    if 'seasons' in tables:
        print("\nSample seasons:")
        result = conn.execute(text("""
            SELECT DISTINCT season_name 
            FROM seasons 
            ORDER BY season_name DESC 
            LIMIT 10;
        """))
        for row in result.fetchall():
            print(f"  - {row[0]}")
    
    # Check teams/clubs
    print("\nSample teams/clubs:")
    result = conn.execute(text("""
        SELECT DISTINCT team_name 
        FROM dim_teams 
        ORDER BY team_name 
        LIMIT 10;
    """))
    for row in result.fetchall():
        print(f"  - {row[0]}")
    
    # Check total counts
    print("\n" + "=" * 60)
    print("DATA COUNTS")
    print("=" * 60)
    
    result = conn.execute(text("SELECT COUNT(*) FROM dim_players"))
    print(f"\nTotal players: {result.fetchone()[0]}")
    
    result = conn.execute(text("SELECT COUNT(*) FROM dim_teams"))
    print(f"Total teams: {result.fetchone()[0]}")
    
    result = conn.execute(text("SELECT COUNT(*) FROM dim_competitions"))
    print(f"Total competitions: {result.fetchone()[0]}")
    
    if 'seasons' in tables:
        result = conn.execute(text("SELECT COUNT(*) FROM seasons"))
        print(f"Total seasons: {result.fetchone()[0]}")

print("\n" + "=" * 60)
print("Check complete!")
print("=" * 60)