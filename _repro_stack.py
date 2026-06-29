import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from streamlit.testing.v1 import AppTest

PAGE = ROOT / "dashboards" / "pages" / "4_🔄_Transfer_Recommendations.py"

at = AppTest.from_file(str(PAGE), default_timeout=60)

# Pre-authenticate so is_authenticated() returns True.
at.session_state["authenticated"] = True
at.session_state["user_id"] = 1
at.session_state["username"] = "admin"
at.session_state["email"] = "admin@example.com"
at.session_state["role"] = "admin"
at.session_state["session_id"] = "test-session-id"
at.session_state["auth_token"] = "test-token"

print("=== RUN 1 (initial page load) ===", flush=True)
at.run()
print("exception:", [str(e.value) for e in at.exception], flush=True)
print("error:", [str(e) for e in at.error], flush=True)
print("num buttons:", len(at.button), flush=True)
for b in at.button:
    print("  button label:", b.label, flush=True)

# Click "Find Similar Players"
clicked = False
for b in at.button:
    if b.label == "Find Similar Players":
        b.click()
        clicked = True
        break

if clicked:
    print("=== RUN 2 (after clicking Find Similar Players) ===", flush=True)
    at.run()
    print("exception:", [str(e.value) for e in at.exception], flush=True)
    print("error values:", [str(e) for e in at.error], flush=True)
    recs = at.session_state["recommendations"] if "recommendations" in at.session_state else None
    print("num recommendations:", len(recs) if recs else 0, flush=True)
    if recs:
        names = [r.get("player_name") for r in recs]
        print("rec names:", names, flush=True)
        seen = set()
        dups = []
        for n in names:
            if n in seen:
                dups.append(n)
            seen.add(n)
        print("duplicate names in recommendations:", dups, flush=True)

    # Button keys actually registered
    btn_keys = [b.key for b in at.button]
    print("num buttons:", len(at.button), flush=True)
    print("button keys:", btn_keys, flush=True)
    seen_k = set()
    dup_keys = []
    for k in btn_keys:
        if k in seen_k:
            dup_keys.append(k)
        seen_k.add(k)
    print("DUPLICATE BUTTON KEYS:", dup_keys, flush=True)

print("=== WARNINGS (render counts) ===", flush=True)
for w in at.warning:
    print("WARN:", w.value, flush=True)

print("=== st.code blocks (stack traces) ===", flush=True)
for i, c in enumerate(at.code):
    print(f"----- st.code #{i} -----", flush=True)
    print(c.value, flush=True)

print("=== DONE ===", flush=True)
