import os
for root, dirs, files in os.walk(r"d:\Sports Intelligence & Analytics Platform"):
    dirs[:] = [d for d in dirs if d not in ("venv", "__pycache__", ".git")]
    for f in files:
        if not f.endswith(".py"):
            continue
        path = os.path.join(root, f)
        try:
            text = open(path, encoding="utf-8").read()
        except Exception:
            continue
        if ".save()" in text:
            print(path)
