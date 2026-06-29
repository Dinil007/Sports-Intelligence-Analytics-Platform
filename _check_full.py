"""
Comprehensive runtime identity & module origin check.
Intended to be run with: .\\venv\\Scripts\\python.exe _check_full.py
Checks: 2, 3, 4, 6, 7, 8
"""
import os, sys, pathlib, subprocess, json

ROOT = pathlib.Path(__file__).resolve().parent

print("=" * 70)
print("CHECK 2: RUNTIME IDENTITY")
print("=" * 70)
print(f"os.getpid()      = {os.getpid()}")
print(f"sys.executable   = {sys.executable}")
print(f"os.getcwd()      = {os.getcwd()}")
print(f"__file__         = {__file__}")
print(f"resolve          = {ROOT}")

# Force imports
sys.path.insert(0, str(ROOT))
import dashboards.components.action_buttons as act
import dashboards.components.recommendation_card as card

print()
print("=" * 70)
print("CHECK 3: MODULE ORIGINS")
print("=" * 70)
targets = [
    ("dashboards.app", "dashboards.app"),
    ("dashboards.components.action_buttons", "dashboards.components.action_buttons"),
    ("dashboards.components.recommendation_card", "dashboards.components.recommendation_card"),
    ("dashboards.pages.4_🔄_Transfer_Recommendations", "dashboards.pages.4_🔄_Transfer_Recommendations"),
]
for label, modname in targets:
    mod = sys.modules.get(modname)
    if mod:
        print(f"  {label}:")
        print(f"    id  = {id(mod)}")
        print(f"    file = {getattr(mod, '__file__', 'MISSING')}")
    else:
        print(f"  {label}: NOT LOADED")

print()
print("=" * 70)
print("CHECK 4: SEARCH FOR ANOTHER 'dashboards' PACKAGE")
print("=" * 70)

# Check site-packages
sp_paths = []
for p in sys.path:
    if 'site-packages' in p.lower():
        sp_paths.append(p)

for sp in sp_paths:
    dash_path = pathlib.Path(sp) / "dashboards"
    if dash_path.exists():
        print(f"  FOUND: {dash_path}")

# pip list
print("\n  --- pip list (grep dashboards) ---")
r = subprocess.run([sys.executable, "-m", "pip", "list", "--format=columns"],
                   capture_output=True, text=True, timeout=30)
for line in r.stdout.splitlines():
    if 'dashboards' in line.lower():
        print(f"    {line}")

# pip show
print("\n  --- pip show dashboards ---")
r2 = subprocess.run([sys.executable, "-m", "pip", "show", "dashboards"],
                    capture_output=True, text=True, timeout=30)
if r2.returncode == 0:
    print(f"    {r2.stdout[:2000]}")
else:
    print("    Not installed via pip")

# Editable installs
print("\n  --- editable installs ---")
r3 = subprocess.run([sys.executable, "-m", "pip", "list", "--editable"],
                    capture_output=True, text=True, timeout=30)
for line in r3.stdout.splitlines():
    if 'dashboards' in line.lower():
        print(f"    {line}")

print()
print("=" * 70)
print("CHECK 6: sys.path (in order)")
print("=" * 70)
for i, p in enumerate(sys.path):
    marker = ""
    if p and os.path.abspath(p) == str(ROOT):
        marker = "  <--- THIS PROJECT ROOT"
    elif p and 'Sports Intelligence' in p:
        marker = "  <--- PROJECT-RELATED PATH"
    print(f"  [{i}] {p}{marker}")

print()
print("=" * 70)
print("CHECK 7: SERVER CONNECTIVITY (for running app)")
print("=" * 70)
# Check what port the running streamlit servers are on
# This is just info - we need to be running to check this
print("  (Run this while server is active for live check)")
print("  Check 7 will be done by querying the running processes")

print()
print("=" * 70)
print("CHECK 8: ANALYSIS")
print("=" * 70)
print("  See stdout for evidence-based conclusions.")
