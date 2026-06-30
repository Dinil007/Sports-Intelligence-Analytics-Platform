import json

# Check match 4020846 raw JSON structure more carefully
with open('data/raw/events/4020846.json') as f:
    data = json.load(f)

# Find a Pass event and inspect its structure
pass_event = next((e for e in data if e.get('type', {}).get('name') == 'Pass'), None)
if pass_event:
    print('Sample Pass event from match 4020846:')
    print(f'  Top-level keys: {sorted(pass_event.keys())}')
    print(f'  location (top-level): {pass_event.get("location")}')
    print(f'  type name: {pass_event.get("type", {}).get("name")}')
    print(f'  pass key exists: {"pass" in pass_event}')
    if "pass" in pass_event:
        print(f'  pass object: {pass_event.get("pass")}')
        print(f'  pass.end_location: {pass_event.get("pass", {}).get("end_location")}')

# Count events with top-level location vs nested location
top_level_loc = sum(1 for e in data if e.get('location') is not None)
nested_pass_loc = sum(1 for e in data if e.get('pass', {}).get('end_location') is not None)
nested_carry_loc = sum(1 for e in data if e.get('carry', {}).get('end_location') is not None)
nested_shot_loc = sum(1 for e in data if e.get('shot', {}).get('end_location') is not None)

print(f'\nLocation count analysis:')
print(f'  Top-level location: {top_level_loc}')
print(f'  Nested pass.end_location: {nested_pass_loc}')
print(f'  Nested carry.end_location: {nested_carry_loc}')
print(f'  Nested shot.end_location: {nested_shot_loc}')

# Check event types with NULL top-level location
events_without_top_loc = [e for e in data if e.get('location') is None]
types_without = {}
for e in events_without_top_loc:
    etype = e.get('type', {}).get('name', 'Unknown')
    types_without[etype] = types_without.get(etype, 0) + 1

print(f'\nEvent types WITHOUT top-level location ({len(events_without_top_loc)} events):')
for etype, count in sorted(types_without.items()):
    print(f'  {etype}: {count}')
