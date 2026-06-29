import os

PATTERNS = [
    "st.rerun(", "st.experimental_rerun(", "st.stop(", "st.switch_page(",
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
            for p in PATTERNS:
                if p in line:
                    hits.append((i, p, line.rstrip()))
        if hits:
            print(f"\n=== {path} ===")
            for i, p, line in hits:
                print(f"  {i}: [{p}] {line}")
