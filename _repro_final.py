"""Comprehensive repro test for duplicate key error."""
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

at.run()

# Click "Find Similar Players"
for b in at.button:
    if b.label == "Find Similar Players":
        b.click()
        break

at.run()
print("RUN 1 (cards render):", [str(e.value) for e in at.exception])

# Simulate selecting a player in the "Compare with..." selectbox
# This simulates what happens when user interacts with the selectbox
# Set the session state as if the user selected "Endrick Felipe Moreira de Sousa"
at.session_state["compare_player_select"] = "Endrick Felipe Moreira de Sousa"

at.run()
print("RUN 2 (selectbox + cards + comparison):", [str(e.value) for e in at.exception])

# Run one more time to see if the error appears on the 3rd visit
at.session_state["compare_player_select"] = "Alan Steve Minda García"
at.run()
print("RUN 3:", [str(e.value) for e in at.exception])

# Check all exceptions
all_exceptions = []
for i in range(4):
    at2 = AppTest.from_file(str(PAGE), default_timeout=60)
    at2.session_state["authenticated"] = True
    at2.session_state["user_id"] = 1
    at2.session_state["username"] = "admin"
    at2.session_state["email"] = "admin@example.com"
    at2.session_state["role"] = "admin"
    at2.session_state["session_id"] = "test-session-id"
    at2.session_state["auth_token"] = "test-token"
    at2.session_state["recommendations"] = at.session_state.get("recommendations", [])
    at2.session_state["selected_player_name"] = at.session_state.get("selected_player_name")
    at2.session_state["has_searched"] = True
    at2.run()
    excs = [str(e.value) for e in at2.exception]
    if excs:
        print(f"NAV VISIT #{i}: exceptions = {excs}")
    else:
        print(f"NAV VISIT #{i}: OK (no exceptions)")

print("\n=== DONE ===", flush=True)
