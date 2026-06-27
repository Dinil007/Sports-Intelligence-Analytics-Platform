"""Simulate Streamlit's import path and check for module identity issues."""

import sys
from pathlib import Path

print(f"sys.argv[0]: {sys.argv}")
print(f"Working dir: {Path.cwd()}")

# Simulate the page file's sys.path manipulation
PROJECT_ROOT = Path(__file__).resolve().parent
print(f"PROJECT_ROOT: {PROJECT_ROOT}")
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

print(f"\nsys.path:")
for i, p in enumerate(sys.path):
    print(f"  {i}: {p}")

print(f"\n--- Step 1: import module ---")
import dashboards.components.recommendation_card as rc
print(f"Module path: {rc.__file__}")
print(f"Module id:   {id(rc)}")
print(f"Module exists in sys.modules: {'dashboards.components.recommendation_card' in sys.modules}")
print(f"sys.modules id: {id(sys.modules['dashboards.components.recommendation_card'])}")
print(f"Same object: {rc is sys.modules['dashboards.components.recommendation_card']}")

print(f"\n--- Step 2: Check available symbols ---")
symbols = sorted(dir(rc))
for s in symbols:
    print(f"  {s}")
print(f"\nrender_recommendation_card in dir: {'render_recommendation_card' in symbols}")
print(f"recommendation_card in dir: {'recommendation_card' in symbols}")

print(f"\n--- Step 3: Try from...import ---")
try:
    from dashboards.components.recommendation_card import render_recommendation_card
    print(f"✅ Import OK: {render_recommendation_card}")
except Exception as e:
    import traceback
    print(f"❌ FAILED: {type(e).__name__}: {e}")
    traceback.print_exc()

print(f"\n--- Step 4: Check sys.modules for duplicates ---")
for name, mod in list(sys.modules.items()):
    if "recommendation_card" in name:
        print(f"  {name} → id={id(mod)}, file={getattr(mod, '__file__', '?')}")

print(f"\n--- Step 5: Verify __pycache__ doesn't bypass ---")
comps_cache = list((PROJECT_ROOT / 'dashboards' / 'components' / '__pycache__').glob('*recommendation_card*'))
print(f"  Pycache files for recommendation_card: {[str(c) for c in comps_cache]}")
