import os

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
        for i, line in enumerate(lines, 1):
            if line.strip().startswith("@st.cache_data") or line.strip().startswith("@st.cache_resource") or line.strip().startswith("@st.experimental_memo") or line.strip().startswith("@st.experimental_singleton"):
                print(f"{path}|{i}|{line.rstrip()}")
