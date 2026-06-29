import os

matches = []
for root, dirs, files in os.walk(r"d:\Sports Intelligence & Analytics Platform"):
    dirs[:] = [d for d in dirs if d not in ("venv", "__pycache__", ".git")]
    for f in files:
        if f.endswith(".py"):
            path = os.path.join(root, f)
            try:
                with open(path, encoding="utf-8") as fh:
                    for i, line in enumerate(fh, 1):
                        if "recommendation_card" in line:
                            matches.append((path, i, line.rstrip()))
            except Exception:
                pass
for path, i, line in matches:
    print(f"{path}|{i}|{line}")
