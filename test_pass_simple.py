from services.match_intelligence_service import get_match_dashboard

dashboard = get_match_dashboard(4020846)
events = dashboard.get("events", [])

successful_passes = [
    e for e in events
    if e.get("event_type") == "Pass"
    and e.get("location") is not None
    and e.get("pass_end_location") is not None
    and (e.get("outcome") is None or "Complete" in str(e.get("outcome")))
]

print(f"Successful passes: {len(successful_passes)}")

# Test each section
print("\n1. Testing list comprehensions (lines 47-48, 78-79):")
try:
    start_x = [e["location"][0] for e in successful_passes]
    start_y = [e["location"][1] for e in successful_passes]
    end_x = [e["pass_end_location"][0] for e in successful_passes]
    end_y = [e["pass_end_location"][1] for e in successful_passes]
    print(f"  OK - created {len(start_x)} start points, {len(end_x)} end points")
except Exception as ex:
    print(f"  FAIL: {type(ex).__name__}: {ex}")

print("\n2. Testing customdata (lines 65-72):")
try:
    customdata = [
        [
            "({:.1f}, {:.1f})".format(e['location'][0], e['location'][1]),
            "({:.1f}, {:.1f})".format(e['pass_end_location'][0], e['pass_end_location'][1]),
            e.get("player_name"),
        ]
        for e in successful_passes
    ]
    print(f"  OK - {len(customdata)} items")
except Exception as ex:
    print(f"  FAIL: {type(ex).__name__}: {ex}")

print("\n3. Testing tuple unpacking (lines 98-99):")
try:
    for i, e in enumerate(successful_passes):
        sx, sy = e["location"]
        ex, ey = e["pass_end_location"]
    print(f"  OK - all {len(successful_passes)} unpacked")
except Exception as ex:
    print(f"  FAIL at event {i}: {type(ex).__name__}: {ex}")
    print(f"     id: {e.get('id')}")
    loc = e.get('location')
    pend = e.get('pass_end_location')
    print(f"     location: {loc} type={type(loc).__name__} len={len(loc) if loc else 'N/A'}")
    print(f"     pass_end_location: {pend} type={type(pend).__name__} len={len(pend) if pend else 'N/A'}")

print("\n4. Testing annotation loop (lines 97-117):")
try:
    for i, e in enumerate(successful_passes[:10]):  # Test first 10
        sx, sy = e["location"]
        ex, ey = e["pass_end_location"]
        mx, my = (sx + ex) / 2, (sy + ey) / 2
    print(f"  OK - annotation math works for first 10 events")
except Exception as ex:
    print(f"  FAIL at event {i}: {type(ex).__name__}: {ex}")

print("\n5. Checking for non-numeric coordinates:")
try:
    for i, e in enumerate(successful_passes):
        loc = e["location"]
        pend = e["pass_end_location"]
        if not all(isinstance(v, (int, float)) for v in loc):
            print(f"  WARNING: event {i} has non-numeric location: {loc}")
            break
        if not all(isinstance(v, (int, float)) for v in pend):
            print(f"  WARNING: event {i} has non-numeric pass_end_location: {pend}")
            break
    else:
        print(f"  OK - all coordinates are numeric")
except Exception as ex:
    print(f"  FAIL: {type(ex).__name__}: {ex}")
