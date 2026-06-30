#!/usr/bin/env python3
"""Trace one event through the complete pipeline."""

from database.match_repository import fetch_match_events
from services.match_intelligence_service import get_match_dashboard
from dashboards.components.pitch_visualizations.pitch_dashboard import render_pitch_dashboard
import json

# Step 1: Read raw StatsBomb JSON
print("=" * 80)
print("STEP 1: RAW STATSBOMB JSON")
print("=" * 80)
with open('data/raw/events/15946.json') as f:
    raw_events = json.load(f)

# Find a Pass event with coordinates
pass_event = next((e for e in raw_events if e.get('type', {}).get('name') == 'Pass' and e.get('location')), None)
if pass_event:
    print(f"Event ID: {pass_event.get('id')}")
    print(f"Type: {pass_event.get('type', {}).get('name')}")
    print(f"Minute: {pass_event.get('minute')}")
    print(f"Player: {pass_event.get('player', {}).get('name')}")
    print(f"Team: {pass_event.get('team', {}).get('name')}")
    print(f"RAW Location: {pass_event.get('location')}")
    print(f"RAW pass_end_location: {pass_event.get('pass_end_location')}")

# Step 2: Query PostgreSQL
print("\n" + "=" * 80)
print("STEP 2: POSTGRESQL QUERY")
print("=" * 80)
from sqlalchemy import text
from database.db_connection import engine

event_id = pass_event.get('id') if pass_event else None
if event_id:
    sql = text('SELECT id, event_type, location_x, location_y, pass_end_x, pass_end_y FROM fact_match_events WHERE id = :eid')
    with engine.connect() as conn:
        row = conn.execute(sql, {'eid': event_id}).mappings().fetchone()
    
    if row:
        print(f"id: {row['id']}")
        print(f"event_type: {row['event_type']}")
        print(f"location_x: {row['location_x']}")
        print(f"location_y: {row['location_y']}")
        print(f"pass_end_x: {row['pass_end_x']}")
        print(f"pass_end_y: {row['pass_end_y']}")

# Step 3: fetch_match_events() return value
print("\n" + "=" * 80)
print("STEP 3: fetch_match_events() RETURN VALUE")
print("=" * 80)
events = fetch_match_events(15946)
print(f"Total events returned: {len(events)}")
if event_id:
    target = [e for e in events if str(e.get('id')) == str(event_id)]
    print(f"Target event found: {len(target) > 0}")
    if target:
        e = target[0]
        print(f"Keys: {sorted(e.keys())}")
        print(f"event_type: {e.get('event_type')}")
        print(f"location: {e.get('location')}")
        print(f"type(location): {type(e.get('location'))}")
        print(f"pass_end_location: {e.get('pass_end_location')}")
        print(f"location_x (not in dict): {'location_x' in e}")
        print(f"location_y (not in dict): {'location_y' in e}")

# Step 4: get_match_dashboard()["events"][0]
print("\n" + "=" * 80)
print("STEP 4: get_match_dashboard()['events'][0]")
print("=" * 80)
dashboard = get_match_dashboard(15946)
all_dashboard_events = dashboard.get("events", [])
print(f"Total events in dashboard: {len(all_dashboard_events)}")
if all_dashboard_events:
    first = all_dashboard_events[0]
    print(f"\nFirst event keys: {sorted(first.keys())}")
    print(f"event_type: {first.get('event_type')}")
    print(f"location: {first.get('location')}")
    print(f"type(location): {type(first.get('location'))}")
    print(f"pass_end_location: {first.get('pass_end_location')}")
    
    # Find our target event
    if event_id:
        target_dash = [e for e in all_dashboard_events if str(e.get('id')) == str(event_id)]
        print(f"\nTarget event in dashboard: {len(target_dash) > 0}")
        if target_dash:
            ed = target_dash[0]
            print(f"event_type: {ed.get('event_type')}")
            print(f"location: {ed.get('location')}")
            print(f"type(location): {type(ed.get('location'))}")
            print(f"pass_end_location: {ed.get('pass_end_location')}")

# Step 5: What pitch_dashboard.py receives
print("\n" + "=" * 80)
print("STEP 5: WHAT pitch_dashboard.py RECEIVES")
print("=" * 80)
# Simulate what pitch_dashboard does
events_for_pitch = dashboard.get("events", [])
print(f"Events passed to pitch_dashboard: {len(events_for_pitch)}")

# Count events by type
from collections import Counter
type_counts = Counter(e.get('event_type') for e in events_for_pitch)
print(f"\nEvent type distribution:")
for etype, count in sorted(type_counts.items()):
    has_loc = sum(1 for e in events_for_pitch if e.get('event_type') == etype and e.get('location') is not None)
    print(f"  {etype}: {count} total, {has_loc} with location")

# Check Pass events specifically
pass_events = [e for e in events_for_pitch if e.get('event_type') == 'Pass']
pass_with_loc = [e for e in pass_events if e.get('location') is not None and e.get('pass_end_location') is not None]
print(f"\nPass events with both location and pass_end_location: {len(pass_with_loc)}")
print(f"Pass events missing coordinates: {len(pass_events) - len(pass_with_loc)}")

# Step 6: WHY "Pitch coordinates are unavailable"
print("\n" + "=" * 80)
print("STEP 6: WHY 'Pitch coordinates are unavailable' IS DISPLAYED")
print("=" * 80)

# Simulate the event filter logic
from dashboards.components.pitch_visualizations.event_filter import render_event_filter
print("\nSimulating event filter for 'Pass':")
filtered = [e for e in events_for_pitch if e.get('event_type') == 'Pass']
print(f"Filtered Pass events: {len(filtered)}")

has_coords = any(
    e.get("location") is not None or (
        e.get("pass_end_location") is not None
        or e.get("carry_end_location") is not None
        or e.get("shot_end_location") is not None
    )
    for e in filtered
)
print(f"Any coordinates in filtered Pass events: {has_coords}")

# Check if the condition in pitch_dashboard.py triggers
if not has_coords:
    print("\n⚠️  CONDITION TRIGGERED: 'not has_any_coordinates' is True")
    print("This causes: st.info('Pitch coordinates are unavailable for this event type.')")
else:
    print("\n✓ Condition NOT triggered - coordinates exist")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
