from services.match_intelligence_service import get_match_dashboard

dash = get_match_dashboard(15946)
events = dash.get('events', [])
types = sorted(set(e.get('event_type') for e in events))
print('Event types in dashboard:')
for t in types:
    count = sum(1 for e in events if e.get('event_type') == t)
    has_loc = sum(1 for e in events if e.get('event_type') == t and e.get('location') is not None)
    print(f'  {t}: {count} events, {has_loc} with location')
    
# Check which event types have NO locations
print('\nEvent types with NO location data:')
for t in types:
    filtered = [e for e in events if e.get('event_type') == t]
    has_any = any(
        e.get("location") is not None or e.get("pass_end_location") is not None or 
        e.get("carry_end_location") is not None or e.get("shot_end_location") is not None
        for e in filtered
    )
    if not has_any:
        print(f'  {t}: NO COORDINATES')
        sample = filtered[0] if filtered else None
        if sample:
            print(f'    Sample keys: {sorted(sample.keys())}')
            print(f'    Sample location fields:')
            for k in ['location', 'pass_end_location', 'carry_end_location', 'shot_end_location', 'pressure_location', 'block_location', 'interception_location', 'clearance_location', 'ball_receipt_location']:
                print(f'      {k}: {sample.get(k)}')
