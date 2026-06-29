"""Full app repro through app.py with multi-page navigation."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from streamlit.testing.v1 import AppTest

PAGE = ROOT / "dashboards" / "app.py"

at = AppTest.from_file(str(PAGE), default_timeout=60)

# Pre-authenticate
at.session_state["authenticated"] = True
at.session_state["user_id"] = 1
at.session_state["username"] = "admin"
at.session_state["email"] = "admin@example.com"
at.session_state["role"] = "admin"
at.session_state["session_id"] = "test-session-id"
at.session_state["auth_token"] = "test-token"

print("=== RUN 1 (app.py login -> redirect to home) ===", flush=True)
at.run()
print("exception:", [str(e.value) for e in at.exception], flush=True)

# Find the "Transfer Recommendations" navigation link and click it
# In AppTest, navigation is handled via st.navigation which is tricky.
# Let's directly set the page to transfer recommendations.

# Actually, let's try a simpler approach - simulate the page being accessed
# by running it directly but with navigation state.

# Create a fresh AppTest for the Transfer Recommendations page
PAGE2 = ROOT / "dashboards" / "pages" / "4_🔄_Transfer_Recommendations.py"
at2 = AppTest.from_file(str(PAGE2), default_timeout=60)

at2.session_state["authenticated"] = True
at2.session_state["user_id"] = 1
at2.session_state["username"] = "admin"
at2.session_state["email"] = "admin@example.com"
at2.session_state["role"] = "admin"
at2.session_state["session_id"] = "test-session-id"
at2.session_state["auth_token"] = "test-token"

print("\n=== RUN 2 (load transfer page) ===", flush=True)
at2.run()
print("exception:", [str(e.value) for e in at2.exception], flush=True)

# Click "Find Similar Players"
clicked = False
for b in at2.button:
    if b.label == "Find Similar Players":
        b.click()
        clicked = True
        break

if clicked:
    print("\n=== RUN 3 (after Find Similar Players) ===", flush=True)
    at2.run()
    print("exception:", [str(e.value) for e in at2.exception], flush=True)
    print("num buttons:", len(at2.button), flush=True)
    
    # Now simulate what happens when a user navigates AWAY and then BACK
    # by running the page again (as if it's a fresh navigation)
    at3 = AppTest.from_file(str(PAGE2), default_timeout=60)
    at3.session_state["authenticated"] = True
    at3.session_state["user_id"] = 1
    at3.session_state["username"] = "admin"
    at3.session_state["email"] = "admin@example.com"
    at3.session_state["role"] = "admin"
    at3.session_state["session_id"] = "test-session-id"
    at3.session_state["auth_token"] = "test-token"
    
    # Copy recommendations from previous run to simulate session persistence
    if "recommendations" in at2.session_state:
        at3.session_state["recommendations"] = at2.session_state["recommendations"]
    if "selected_player_name" in at2.session_state:
        at3.session_state["selected_player_name"] = at2.session_state["selected_player_name"]
    if "compare_player" in at2.session_state:
        at3.session_state["compare_player"] = at2.session_state["compare_player"]
    at3.session_state["has_searched"] = True
    
    print("\n=== RUN 4 (simulate navigation back to transfer page) ===", flush=True)
    at3.run()
    print("exception:", [str(e.value) for e in at3.exception], flush=True)
    
    # Collect button keys
    btn_keys = [b.key for b in at3.button]
    seen_k = set()
    dup_keys = []
    for k in btn_keys:
        if k in seen_k:
            dup_keys.append(k)
        seen_k.add(k)
    print("num buttons:", len(at3.button), flush=True)
    print("DUPLICATE BUTTON KEYS:", dup_keys, flush=True)
    
    # Check for exceptions
    if at3.exception:
        print("EXCEPTIONS:", flush=True)
        for e in at3.exception:
            print(f"  {type(e.value).__name__}: {e.value}", flush=True)

print("\n=== DONE ===", flush=True)
