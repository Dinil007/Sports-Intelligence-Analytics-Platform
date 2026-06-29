"""
Check 1: Process verification
==============================
- List all python.exe processes
- List all streamlit processes  
- Print the command line used to launch each process
"""
import psutil, os

print("=" * 70)
print("CHECK 1: RUNNING PYTHON & STREAMLIT PROCESSES")
print("=" * 70)

for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
    try:
        info = proc.info
        name = (info['name'] or '').lower()
        cmdline = info['cmdline']
        cmd_str = ' '.join(cmdline) if cmdline else ''
        
        # python.exe OR anything mentioning streamlit
        if 'python' in name or 'streamlit' in cmd_str.lower():
            print(f"\nPID: {info['pid']}")
            print(f"Name: {info['name']}")
            print(f"Cmd: {cmd_str}")
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

print("\n--- end check 1 ---")
