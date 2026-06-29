"""
Second-pass investigation: verify PID 4204 is the same process,
check parent's environment, and test if PID 4204 can actually import streamlit.
"""
import psutil, os, sys, subprocess, time

PARENT_PID = 33596
CHILD_PID = 4204

print("=" * 70)
print("PASS 2: DEEP VERIFICATION")
print("=" * 70)

# Is PID 4204 still running?
print("\n--- A. Is PID 4204 still alive? ---")
try:
    p = psutil.Process(CHILD_PID)
    print("PID 4204 is ALIVE")
    print("  name():", p.name())
    print("  exe():", p.exe())
    print("  create_time():", p.create_time())
except psutil.NoSuchProcess:
    print("PID 4204 is DEAD - it was recycled!")
    sys.exit(1)

# Is PID 33596 still running?
print("\n--- B. Is PID 33596 still alive? ---")
try:
    parent = psutil.Process(PARENT_PID)
    print("PID 33596 is ALIVE")
    print("  name():", parent.name())
    print("  exe():", parent.exe())
    print("  create_time():", parent.create_time())
except psutil.NoSuchProcess:
    print("PID 33596 is DEAD")

# Compare create times
print("\n--- C. Parent/Child creation time comparison ---")
if psutil.Process(CHILD_PID).create_time() == psutil.Process(PARENT_PID).create_time():
    print("⚠️  SAME CREATE TIME - possible PID reuse")
else:
    print("Different create times - parent predates child (expected)")

# Parent's environment
print("\n--- D. Parent PID 33596 environment ---")
try:
    penv = parent.environ()
    for key in ['PATH', 'PYTHONHOME', 'PYTHONPATH', 'VIRTUAL_ENV']:
        val = penv.get(key, '<NOT SET>')
        print(f"  {key}: {val[:200] if len(val) > 200 else val}")
except Exception as e:
    print("  ERROR:", e)

# Child's environment again, with more detail
print("\n--- E. Child PID 4204 environment (full) ---")
try:
    cenv = p.environ()
    print("  Total env vars:", len(cenv))
    for key in ['PATH', 'PYTHONHOME', 'PYTHONPATH', 'VIRTUAL_ENV']:
        val = cenv.get(key, '<NOT SET>')
        print(f"  {key}: {val[:300] if len(val) > 300 else val}")
except Exception as e:
    print("  ERROR:", e)

# Try to see if PID 4204 can actually import streamlit
print("\n--- F. Can PID 4204 import streamlit? ---")
# We can't inject code directly, but we can check file handles
# Look for .pyc files or __pycache__ in open files
try:
    of = p.open_files()
    pyfiles = [f.path for f in of if f.path.endswith('.py') or f.path.endswith('.pyc')]
    print("  Python files opened by PID 4204:")
    for f in pyfiles[:20]:
        print("    ", f)
except Exception as e:
    print("  ERROR:", e)

# Memory maps - look for loaded DLLs/modules
print("\n--- G. PID 4204 memory maps containing 'python' or 'streamlit' ---")
try:
    maps = p.memory_maps()
    interesting = [m.path for m in maps if m.path and ('python' in m.path.lower() or 'streamlit' in m.path.lower() or 'dashboards' in m.path.lower())]
    for m in interesting[:30]:
        print("  ", m)
except Exception as e:
    print("  ERROR:", e)

# Check if there's another python.exe in sys.path order that has streamlit
print("\n--- H. Where would PID 4204 find streamlit? ---")
# Simulate: what's first on PATH?
path_val = cenv.get('PATH', '')
path_dirs = path_val.split(';')
for d in path_dirs:
    if 'python' in d.lower() or 'python312' in d.lower():
        candidate = os.path.join(d, 'Lib', 'site-packages', 'streamlit')
        if os.path.exists(candidate):
            print(f"  FOUND streamlit at: {candidate}")
        else:
            print(f"  No streamlit at: {candidate}")

# Also check if current working directory has streamlit
cwd = p.cwd()
print(f"  CWD of PID 4204: {cwd}")
local_streamlit = os.path.join(cwd, 'streamlit')
print(f"  Local streamlit exists: {os.path.exists(local_streamlit)}")

print("\n--- END PASS 2 ---")
