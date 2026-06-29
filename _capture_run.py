import subprocess, sys, os, time, signal

page = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "dashboards", "pages", "4_🔄_Transfer_Recommendations.py")

with open("d:\\stderr_instrumented.txt", "w") as ferr:
    proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", page,
         "--server.headless", "true",
         "--server.port", "8502",
         "--server.enableCORS", "false",
         "--server.enableXsrfProtection", "false"],
        stdout=subprocess.DEVNULL,
        stderr=ferr,
    )
    print("PID:", proc.pid)
    # Wait for the app to start and be probed
    # The app is started, now we wait for user interaction or just probe it
    time.sleep(15)
    # Kill it
    proc.terminate()
    proc.wait(timeout=5)
    print("Done.")
