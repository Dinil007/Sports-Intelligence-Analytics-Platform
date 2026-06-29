import pathlib, re
root = pathlib.Path(r"d:\Sports Intelligence & Analytics Platform\dashboards\pages")
for p in root.glob("*.py"):
    text = p.read_text(encoding="utf-8")
    if "st.set_page_config" in text:
        print(p.name, "YES")
    else:
        print(p.name, "NO")
