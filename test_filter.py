from services.match_intelligence_service import get_match_dashboard

# Simulate what pitch_dashboard.py does
match_dashboard = get_match_dashboard(15946)
events = match_dashboard.get("events", [])

# Test each filter option
filters = ["All", "Pass", "Carry", "Shot", "Pressure", "Recovery", "Tackle", "Interception", "Block", "Clearance"]

filter_map = {
    "Recovery": "Ball Recovery",
    "Tackle": "Tackle",
    "Interception": "Interception",
    "Block": "Block",
    "Clearance": "Clearance",
}

print("Testing each event filter option:")
print("=" * 80)
for event_type in filters:
    if event_type == "All":
        filtered = events
    else:
        target_type = filter_map.get(event_type, event_type)
        filtered = [e for e in events if e.get("event_type") == target_type]
    
    print(f"\nFilter: '{event_type}' → {len(filtered)} events")
    
    if not filtered:
        print(f"  ⚠️  NO EVENTS - would show: 'No events available for pitch visualizations.'")
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
        print(f"  ⚠️  WOULD SHOW: 'Pitch coordinates are unavailable for this event type.'")
        # Show sample
        sample = filtered[0]
        print(f"  Sample: event_type={sample.get('event_type')}, location={sample.get('location')}")
    else:
        print(f"  ✓ Has coordinates - would render visualizations")
