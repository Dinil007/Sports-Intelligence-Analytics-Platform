"""
Investigate PID 4204 with full runtime evidence.
Requires: psutil (available in venv)
"""
import psutil, os, sys, subprocess

TARGET_PID = 4204

print("=" * 70)
print("INVESTIGATING PID 4204")
print("=" * 70)

# 1. COMPLETE command line
print("\n--- 1. COMPLETE command line ---")
try:
    p = psutil.Process(TARGET_PID)
    cmdline = p.cmdline()
    print("cmdline:", cmdline)
    print("joined: ", " ".join(cmdline))
except Exception as e:
    print("ERROR:", e)

# 2. Is it actually python -m streamlit run dashboards/app.py?
print("\n--- 2. Command analysis ---")
try:
    full = " ".join(p.cmdline()).lower()
    print("Contains 'python.exe':", "python.exe" in full)
    print("Contains '-m streamlit':", "-m streamlit" in full)
    print("Contains 'run dashboards':", "run dashboards" in full)
    print("Contains 'app.py':", "app.py" in full)
    # Look for any other indicators
    if "streamlit" in full:
        print("STREAMLIT PRESENT IN CMDLINE")
    else:
        print("WARNING: STREAMLIT NOT IN CMDLINE")
except Exception as e:
    print("ERROR:", e)

# 3. Environment variables
print("\n--- 3. Environment variables ---")
try:
    env = p.environ()
    for key in ['PATH', 'PYTHONHOME', 'PYTHONPATH', 'VIRTUAL_ENV']:
        val = env.get(key, '<NOT SET>')
        print(f"{key}: {val}")
except Exception as e:
    print("ERROR accessing environ():", e)

# 4. Open files and loaded DLLs
print("\n--- 4. Open files / loaded libraries ---")
try:
    files = p.open_files()
    interesting = [f.path for f in files if 'streamlit' in f.path.lower() or 'dashboards' in f.path.lower()]
    print("Files containing 'streamlit' or 'dashboards':")
    for f in interesting[:20]:
        print("  ", f)
except Exception as e:
    print("ERROR:", e)

# 5. Memory maps / loaded modules
print("\n--- 5. Memory maps ---")
try:
    maps = p.memory_maps()
    streamlit_maps = [m.path for m in maps if 'streamlit' in m.path.lower()]
    dashboards_maps = [m.path for m in maps if 'dashboards' in m.path.lower()]
    print("Memory maps containing 'streamlit':")
    for m in streamlit_maps[:20]:
        print("  ", m)
    print("Memory maps containing 'dashboards':")
    for m in dashboards_maps[:20]:
        print("  ", m)
except Exception as e:
    print("ERROR:", e)

# 6. Try to determine the executable being run
print("\n--- 6. Process executable details ---")
try:
    exe = p.exe()
    print("exe():", exe)
    print("name():", p.name())
    print("pid:", p.pid)
    print("ppid:", p.ppid())
except Exception as e:
    print("ERROR:", e)

# 7. Check parent process details
print("\n--- 7. Parent process (PID 33596) ---")
try:
    parent = psutil.Process(p.ppid())
    print("Parent name:", parent.name())
    print("Parent exe:", parent.exe())
    print("Parent cmdline:", parent.cmdline())
except Exception as e:
    print("ERROR:", e)

# 8. Create a small test: can we run the same command and see what streamlit loads?
print("\n--- 8. Simulating PID 4204's python -c 'import streamlit' ---")
try:
    # Try to find python.exe from PATH using same method as normal
    # First, check if 'python' resolves to something
    result = subprocess.run(
        ["where", "python"],
        capture_output=True, text=True, timeout=10
    )
    print("where python:")
    for line in result.stdout.strip().splitlines():
        print("  ", line)
except Exception as e:
    print("ERROR:", e)

print("\n--- END OF INVESTIGATION ---")
