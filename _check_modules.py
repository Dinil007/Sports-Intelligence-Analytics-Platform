"""
Check 2: Runtime identity probes + Check 3: Module origins + Check 6: sys.path
"""

import os, sys, pathlib

print("=" * 70)
print(f"os.getpid()      = {os.getpid()}")
print(f"sys.executable   = {sys.executable}")
print(f"os.getcwd()      = {os.getcwd()}")
print(f"__file__         = {__file__}")
print(f"resolve          = {pathlib.Path(__file__).resolve()}")
print("=" * 70)

# Check 3: Module origins
modules_to_check = [
    "dashboards.components.action_buttons",
    "dashboards.components.recommendation_card",
    "dashboards.pages.4_🔄_Transfer_Recommendations",
]

for mod_name in modules_to_check:
    mod = sys.modules.get(mod_name)
    if mod:
        print(f"\n{mod_name}:")
        print(f"  id(module) = {id(mod)}")
        print(f"  __file__   = {getattr(mod, '__file__', 'NO __file__')}")
    else:
        print(f"\n{mod_name}: NOT LOADED")

# Check 6: sys.path
print("\n" + "=" * 70)
print("sys.path (in order)")
print("=" * 70)
for i, p in enumerate(sys.path):
    marker = "  <--- PROJECT ROOT" if p and os.path.abspath(p) == pathlib.Path(__file__).resolve().parent.as_posix().replace('/', '\\') else ""
    print(f"  [{i}] {p}{marker}")
