import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from streamlit.testing.v1 import AppTest

PAGE = ROOT / "dashboards" / "pages" / "4_🔄_Transfer_Recommendations.py"

at = AppTest.from_file(str(PAGE), default_timeout=60)

at.session_state["authenticated"] = True
at.session_state["user_id"] = 1
at.session_state["username"] = "admin"
at.session_state["email"] = "admin@example.com"
at.session_state["role"] = "admin"
at.session_state["session_id"] = "test-session-id"
at.session_state["auth_token"] = "test-token"

print("=== RUN 1 (initial) ===", flush=True)
at.run()
print("exception:", [str(e.value) for e in at.exception], flush=True)

# Click Find Similar Players
for b in at.button:
    if b.label == "Find Similar Players":
        b.click()
        break

print("=== RUN 2 (after click) ===", flush=True)
at.run()
print("exception:", [str(e.value) for e in at.exception], flush=True)

recs = at.session_state["recommendations"] if "recommendations" in at.session_state else []
print("num recommendations:", len(recs), flush=True)

# --- Loop-entry stack trace (st.code emitted by our instrumented page) ---
loop_codes = [c for c in at.code]
print(f"\n=== LOOP ENTRY STACKS ({len(loop_codes)}) ===", flush=True)
for i, c in enumerate(loop_codes):
    print(f"\n----- LOOP ENTRY #{i} -----", flush=True)
    print(c.value, flush=True)

# --- identify which code block is "ENTER LOOP" vs card-level ---
# st.write("ENTER LOOP") becomes markdown in AppTest, but we captured all st.code
# Each card also emits an st.code at the very top of render_recommendation_card.

# Gather card-level st.code blocks and filter by presence of render_recommendation_card in stack
card_codes = []
for c in at.code:
    v = c.value
    if "render_recommendation_card" in v:
        card_codes.append(v)

print(f"\n=== CARD-LEVEL STACKS (found {len(card_codes)}) ===", flush=True)
# Print first 3 for Endrick
endrick_codes = [v for v in card_codes if "Endrick" in v]
print("Endrick card-level traces:", len(endrick_codes), flush=True)
for i, v in enumerate(endrick_codes[:3], 1):
    print(f"\n----- Endrick TRACE #{i} -----", flush=True)
    print(v, flush=True)

# ids of list and recs
print("\n=== IDS ===", flush=True)
if recs:
    print("id(recommendations list):", id(recs), flush=True)
    owners = {}
    for rec in recs:
        name = rec.get("player_name", "Unknown")
        owners.setdefault(name, []).append(id(rec))
    for name, ids in owners.items():
        print(f"  {name}: rec ids = {ids}", flush=True)

print("\n=== DONE ===", flush=True)
