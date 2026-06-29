"""
Pass 3: Map port 8501 to actual process with 100% certainty.
Check ALL listening sockets and ALL python processes.
Also test HTTP response from port 8501.
"""
import psutil, socket, time

print("=" * 70)
print("PASS 3: PORT 8501 → PROCESS MAPPING")
print("=" * 70)

# 1. All listening TCP sockets
print("\n--- 1. All LISTENING TCP sockets with PID ---")
for conn in psutil.net_connections(kind='tcp'):
    if conn.laddr and conn.laddr.port == 8501 and conn.status == psutil.CONN_LISTEN:
        print(f"  LISTEN {conn.laddr.ip}:{conn.laddr.port}  PID={conn.pid}")
        try:
            p = psutil.Process(conn.pid)
            print(f"    Process: {p.name()}  exe={p.exe()}")
            print(f"    cmdline: {p.cmdline()}")
        except Exception as e:
            print(f"    ERROR: {e}")

# 2. All ESTABLISHED connections on port 8501
print("\n--- 2. All ESTABLISHED TCP connections on port 8501 ---")
for conn in psutil.net_connections(kind='tcp'):
    if (conn.laddr and conn.laddr.port == 8501) or (conn.raddr and conn.raddr.port == 8501):
        print(f"  {conn.status}: {conn.laddr.ip}:{conn.laddr.port} <-> {conn.raddr.ip}:{conn.raddr.port}  PID={conn.pid}  LOCAL_PID={conn.pid}")
        try:
            p = psutil.Process(conn.pid)
            print(f"    Process: {p.name()}  exe={p.exe()}")
        except:
            pass

# 3. All python processes with their parent relationships
print("\n--- 3. ALL python.exe processes with parents ---")
for p in psutil.process_iter(['pid', 'name', 'exe', 'cmdline', 'ppid', 'create_time']):
    try:
        if 'python' in p.info['name'].lower():
            ppid = p.info['ppid']
            try:
                parent = psutil.Process(ppid)
                parent_name = parent.name()
            except:
                parent_name = "?"
            
            print(f"  PID={p.info['pid']}  PPID={ppid}  Parent={parent_name}")
            print(f"    exe: {p.info['exe']}")
            print(f"    cmd: {' '.join(p.info['cmdline'])}")
            
            # Check if it's listening
            for conn in p.connections(kind='tcp'):
                if conn.status == psutil.CONN_LISTEN:
                    print(f"    LISTENING on port {conn.laddr.port}")
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

# 4. Actually fetch HTTP from port 8501 and see what handles it
print("\n--- 4. HTTP probe of localhost:8501 ---")
try:
    import urllib.request
    req = urllib.request.urlopen("http://localhost:8501", timeout=5)
    print(f"  Response: {req.status}")
    print(f"  Headers: {dict(req.headers)}")
    body = req.read(200).decode('utf-8', errors='replace')
    print(f"  Body snippet: {body[:200]}")
except Exception as e:
    print(f"  ERROR: {e}")

# 5. Check if there are any other processes that might be the real server
print("\n--- 5. All processes with open port 8501 connections ---")
for p in psutil.process_iter(['pid', 'name']):
    try:
        for conn in p.connections(kind='tcp'):
            if conn.laddr and conn.laddr.port == 8501:
                print(f"  PID={p.info['pid']}  Name={p.info['name']}  Status={conn.status}")
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

# 6. Verify PID 4204 vs PID 33596 memory maps more carefully
print("\n--- 6. PID 4204 ALL memory maps (filtered) ---")
try:
    p4204 = psutil.Process(4204)
    maps = p4204.memory_maps()
    interesting = [m.path for m in maps if m.path and ('.pyd' in m.path or '.dll' in m.path or 'site-packages' in m.path)]
    for m in interesting:
        if 'streamlit' in m.lower() or 'altair' in m.lower() or 'protobuf' in m.lower() or 'tornado' in m.lower():
            print(f"  STREAMLIT-RELATED: {m}")
    print(f"  Total memory maps: {len(maps)}")
    print(f"  Streamlit-related maps: {sum(1 for m in maps if 'streamlit' in m.path.lower())}")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n--- 7. PID 33596 ALL memory maps (streamlit check) ---")
try:
    p33596 = psutil.Process(33596)
    maps = p33596.memory_maps()
    streamlit_maps = [m.path for m in maps if 'streamlit' in m.path.lower()]
    print(f"  Streamlit maps: {len(streamlit_maps)}")
    for m in streamlit_maps[:10]:
        print(f"    {m}")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n--- END PASS 3 ---")
