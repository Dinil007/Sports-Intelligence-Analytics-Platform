import os

HITS = [
    "st.fragment", "st.experimental_fragment", "st.tabs", "st.empty",
    "st.container", "st.columns", "st.dialog", "st.popover",
    "st.form", "st.expander",
]

for root, dirs, files in os.walk(r"d:\Sports Intelligence & Analytics Platform"):
    dirs[:] = [d for d in dirs if d not in ("venv", "__pycache__", ".git")]
    for f in files:
        if not f.endswith(".py"):
            continue
        path = os.path.join(root, f)
        try:
            lines = open(path, encoding="utf-8").read().splitlines()
        except Exception:
            continue
        hits = []
        for i, line in enumerate(lines, 1):
            for h in HITS:
                if h in line:
                    hits.append((i, line.rstrip(), h))
        if hits:
            print(f"\n=== {path} ===")
            for i, line, h in hits:
                print(f"  {i}: [{h}] {line}")
