from services.match_intelligence_service import get_match_dashboard
from database.match_repository import fetch_matches

matches = fetch_matches()
print(f"Total matches: {len(matches)}")
print("\nTesting first 5 matches for coordinate availability:")

for i, m in enumerate(matches[:5]):
    mid = m['match_id']
    dash = get_match_dashboard(mid)
    events = dash.get('events', [])
    
    if not events:
        print(f"\nMatch {mid}: NO EVENTS")
        continue
    
    filter_map = {
        "Recovery": "Ball Recovery",
        "Tackle": "Tackle",
    }
    
    print(f"\n{'='*80}")
    print(f"Match {mid}: {m['home_team']} vs {m['away_team']}")
    print(f"Total events: {len(events)}")
    
    filters = ["All", "Pass", "Carry", "Shot", "Pressure", "Recovery", "Tackle", "Interception", "Block", "Clearance"]
    issues_found = []
    
    for event_type in filters:
        if event_type == "All":
            filtered = events
        else:
            target_type = filter_map.get(event_type, event_type)
            filtered = [e for e in events if e.get("event_type") == target_type]
        
        if not filtered:
            continue
        
        has_any_coordinates = any(
            e.get("location") is not None or (
                e.get("pass_end_location") is not None
                or e.get("carry_end_location") is not None
                or e.get("shot_end_location") is not None
            )
            for e in filtered
        )
        
        if not has_any_coordinates:
            issues_found.append(event_type)
            print(f"  ⚠️  '{event_type}': {len(filtered)} events but NO coordinates")
    
    if not issues_found:
        print(f"  ✓ All filter options have coordinates")
