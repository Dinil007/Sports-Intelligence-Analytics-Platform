"""Replace invalid st.switch_page("dashboards/app.py") with st.stop()
in all pages, and fix auth/page_guard.py."""
from pathlib import Path

pages_dir = Path("dashboards/pages")
guard_file = Path("auth/page_guard.py")

old = 'st.switch_page("dashboards/app.py")'
new = "st.stop()"

for f in sorted(pages_dir.glob("*.py")):
    text = f.read_text(encoding="utf-8")
    if old in text:
        text = text.replace(old, new)
        f.write_text(text, encoding="utf-8")
        print(f"PATCHED {f.name}")
    else:
        print(f"SKIP {f.name} (no match)")

# Fix page_guard.py
if guard_file.exists():
    text = guard_file.read_text(encoding="utf-8")
    old_guard = 'st.switch_page(redirect_path)'
    if old_guard in text:
        text = text.replace(old_guard, "st.stop()")
        guard_file.write_text(text, encoding="utf-8")
        print("PATCHED auth/page_guard.py")
