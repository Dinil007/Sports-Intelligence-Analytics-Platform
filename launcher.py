# tmp launcher: start Streamlit in background, probe HTML, then terminate

import multiprocessing
import time
import urllib.request
import subprocess
import sys
import os

PORT = 8502
PAGE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "dashboards",
    "pages",
    "4_🔄_Transfer_Recommendations.py",
)

def run_streamlit(_port, page):
    subprocess.run(
        [
            sys.executable, "-m", "streamlit", "run", page,
            "--server.headless", "true",
            "--server.port", str(_port),
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

proc = multiprocessing.Process(target=run_streamlit, args=(PORT, PAGE))
proc.start()
print("[launcher] PID=%d :%d ..." % (proc.pid, PORT), flush=True)

deadline = time.time() + 20
while time.time() < deadline:
    try:
        resp = urllib.request.urlopen("http://localhost:%d" % PORT, timeout=3)
        html = resp.read().decode("utf-8", errors="replace")
        print("[launcher] HTTP %d, %d bytes" % (resp.status, len(html)))
        print("AI_SCOUT_REPORT_IN_HTML:", "AI Scout Report" in html)
        idx = html.find("AI Scout Report")
        if idx >= 0:
            print("--- snippet ---")
            print(html[max(0, idx - 300):idx + 500])
        else:
            print("[launcher] EXPANDER TEXT NOT FOUND")
        break
    except Exception as exc:
        print("  probe failed: %s" % exc)
        time.sleep(0.8)
else:
    print("[launcher] TIMEOUT")

proc.terminate()
proc.join(timeout=5)
print("[launcher] Done.")
