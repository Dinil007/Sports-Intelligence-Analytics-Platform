from database.match_repository import fetch_match_events
from services.match_intelligence_service import get_match_dashboard
import json

# Step 1: Raw StatsBomb
print("=" * 80)
print("STEP 1: RAW STATSBOMB JSON")
print("=" * 80)
with open('data/raw/events/15946.json') as f:
    raw_events = json.load(f)
pe = next((e for e in raw_events if e.get('type',{}).get('name')=='Pass' and e.get('location')), None)
print(f"Event ID: {pe.get('id')}")
print(f"Minute: {pe.get('minute')}")
print(f"Player: {pe.get('player',{}).get('name')}")
print(f"Team: {pe.get('team',{}).get('name')}")
print(f"Location: {pe.get('location')}")
print(f"pass_end_location: {pe.get('pass_end_location')}")

# Step 2: PostgreSQL
print("\n" + "=" * 80)
print("STEP 2: POSTGRESQL")
print("=" * 80)
from sqlalchemy import text
from database.db_connection import engine
eid = pe.get('id')
sql = text('SELECT id, event_type, location_x, location_y, pass_end_x, pass_end_y FROM fact_match_events WHERE id = :eid')
conn = engine.connect()
row = conn.execute(sql, {'eid': eid}).mappings().fetchone()
conn.close()
print(f"id: {row['id']}")
print(f"event_type: {row['event_type']}")
print(f"location_x: {row['location_x']}")
print(f"location_y: {row['location_y']}")
print(f"pass_end_x: {row['pass_end_x']}")
print(f"pass_end_y: {row['pass_end_y']}")

# Step 3: fetch_match_events()
print("\n" + "=" * 80)
print("STEP 3: fetch_match_events() RETURN VALUE")
print("=" * 80)
events = fetch_match_events(15946)
target = [e for e in events if str(e.get('id')) == str(eid)]
print(f"Total events: {len(events)}")
print(f"Target found: {len(target) > 0}")
if target:
    e = target[0]
    print(f"event_type: {e.get('event_type')}")
    print(f"location: {e.get('location')}")
    print(f"type(location): {type(e.get('location'))}")
    print(f"pass_end_location: {e.get('pass_end_location')}")

# Step 4: get_match_dashboard()["events"]
print("\n" + "=" * 80)
print("STEP 4: get_match_dashboard()['events']")
print("=" * 80)
dashboard = get_match_dashboard(15946)
dash_events = dashboard.get("events", [])
target = [e for e in dash_events if str(e.get('id')) == str(eid)]
print(f"Total events: {len(dash_events)}")
print(f"Target found: {len(target) > 0}")
if target:
    e = target[0]
    print(f"event_type: {e.get('event_type')}")
    print(f"location: {e.get('location')}")
    print(f"type(location): {type(e.get('location'))}")
    print(f"pass_end_location: {e.get('pass_end_location')}")

# Step 5: Event type distribution
print("\n" + "=" * 80)
print("STEP 5: EVENT TYPE DISTRIBUTION IN dashboard['events']")
print("=" * 80)
from collections import Counter
type_counts = Counter(e.get('event_type') for e in dash_events)
for etype, count in sorted(type_counts.items()):
    has_loc = sum(1 for e in dash_events if e.get('event_type') == etype and e.get('location') is not None)
    print(f"  {etype}: {count} total, {has_loc} with location")

# Step 6: Simulate pitch_dashboard logic
print("\n" + "=" * 80)
print("STEP 6: SIMULATE pitch_dashboard.py LOGIC")
print("=" * 80)
event_type = 'Pass'
filtered = [e for e in dash_events if e.get('event_type') == event_type]
print(f"Filtered '{event_type}' events: {len(filtered)}")

has_coords = any(
    e.get("location") is not None or (
        e.get("pass_end_location") is not None
        or e.get("carry_end_location") is not None
        or e.get("shot_end_location") is not None
    )
    for e in filtered
)
print(f"Any coordinates in filtered events: {has_coords}")

if not has_coords:
    print("\n⚠️  CONDITION TRIGGERED: 'not has_any_coordinates' is True")
    print("Message: 'Pitch coordinates are unavailable for this event type.'")
else:
    print("\n✓ Condition NOT triggered")

# Check all event types
print("\n" + "=" * 80)
print("STEP 7: CHECK ALL EVENT TYPES FOR COORDINATES")
print("=" * 80)
for etype in ['Pass', 'Carry', 'Shot', 'Pressure', 'Recovery', 'Tackle', 'Interception', 'Block', 'Clearance']:
    filtered = [e for e in dash_events if e.get('event_type') == etype]
    if filtered:
        has_any = any(
            e.get("location") is not None or (
                e.get("pass_end_location") is not None
                or e.get("carry_end_location") is not None
                or e.get("shot_end_location") is not None
            )
            for e in filtered
        )
        sample = filtered[0]
        print(f"{etype}: {len(filtered)} events, has_coords={has_any}")
        print(f"  Sample location: {sample.get('location')}")
        print(f"  Sample pass_end_location: {sample.get('pass_end_location')}")
        print(f"  Sample carry_end_location: {sample.get('carry_end_location')}")
        print(f"  Sample shot_end_location: {sample.get('shot_end_location')}")
