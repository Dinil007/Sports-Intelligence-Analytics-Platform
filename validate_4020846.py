from services.match_intelligence_service import get_match_dashboard

d = get_match_dashboard(4020846)
evts = d.get('events', [])
print(f'Total events: {len(evts)}')
print(f'With location: {sum(1 for e in evts if e.get("location") is not None)}')

# Check Pass events (most important for pitch viz)
pass_evts = [e for e in evts if e.get('event_type') == 'Pass']
has_coords = any(
    e.get('location') is not None or e.get('pass_end_location') is not None
    for e in pass_evts
)
print(f'Pass events: {len(pass_evts)}, has_coords: {has_coords}')

# Check if pitch_dashboard condition would pass
filtered = pass_evts
has_any_coords = any(
    e.get("location") is not None or (
        e.get("pass_end_location") is not None
        or e.get("carry_end_location") is not None
        or e.get("shot_end_location") is not None
    )
    for e in filtered
)
print(f'pitch_dashboard condition (Pass): {has_any_coords}')
