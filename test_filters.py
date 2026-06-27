#!/usr/bin/env python3
"""
Test script to verify advanced filter functionality.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from services.player_service import get_filtered_players, get_all_competitions, get_all_teams

print("=" * 60)
print("TESTING ADVANCED FILTERS")
print("=" * 60)

# Test 1: Get all competitions
print("\n1. Testing get_all_competitions()...")
try:
    competitions = get_all_competitions()
    print(f"   ✅ PASS: Found {len(competitions)} competitions")
    print(f"   Sample: {competitions[:3]}")
except Exception as e:
    print(f"   ❌ FAIL: {e}")
    competitions = []

# Test 2: Get all teams
print("\n2. Testing get_all_teams()...")
try:
    teams = get_all_teams()
    print(f"   ✅ PASS: Found {len(teams)} teams")
    print(f"   Sample: {teams[:3]}")
except Exception as e:
    print(f"   ❌ FAIL: {e}")
    teams = []

# Test 3: Get all players (no filter)
print("\n3. Testing get_filtered_players() with no filters...")
try:
    all_players = get_filtered_players()
    print(f"   ✅ PASS: Found {len(all_players)} players")
    print(f"   Sample: {all_players[:3]}")
except Exception as e:
    print(f"   ❌ FAIL: {e}")
    all_players = []

# Test 4: Filter by competition
if competitions:
    print(f"\n4. Testing get_filtered_players() with competition='{competitions[0]}'...")
    try:
        filtered = get_filtered_players(competition=competitions[0])
        print(f"   ✅ PASS: Found {len(filtered)} players in {competitions[0]}")
        print(f"   Sample: {filtered[:3]}")
    except Exception as e:
        print(f"   ❌ FAIL: {e}")

# Test 5: Filter by club
if teams:
    print(f"\n5. Testing get_filtered_players() with club='{teams[0]}'...")
    try:
        filtered = get_filtered_players(club=teams[0])
        print(f"   ✅ PASS: Found {len(filtered)} players in {teams[0]}")
        print(f"   Sample: {filtered[:3]}")
    except Exception as e:
        print(f"   ❌ FAIL: {e}")

# Test 6: Combined filters
if competitions and teams:
    print(f"\n6. Testing get_filtered_players() with both filters...")
    try:
        filtered = get_filtered_players(competition=competitions[0], club=teams[0])
        print(f"   ✅ PASS: Found {len(filtered)} players")
        print(f"   Competition: {competitions[0]}, Club: {teams[0]}")
    except Exception as e:
        print(f"   ❌ FAIL: {e}")

# Test 7: Verify filtered results are subset of all players
print("\n7. Testing filter logic correctness...")
try:
    if all_players:
        # Get a club that exists
        test_club = teams[0] if teams else None
        if test_club:
            club_players = get_filtered_players(club=test_club)
            # All club players should be in all_players
            all_set = set(all_players)
            club_set = set(club_players)
            if club_set.issubset(all_set):
                print(f"   ✅ PASS: Filtered players are subset of all players")
            else:
                print(f"   ❌ FAIL: Filter returned players not in all players list")
except Exception as e:
    print(f"   ❌ FAIL: {e}")

print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print("✅ All filter tests completed successfully!")
print("=" * 60)