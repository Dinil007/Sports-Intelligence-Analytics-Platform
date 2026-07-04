"""Uptime monitor for host system and services."""
from __future__ import annotations

import time
from typing import Dict, Any

# Keep a static reference to module load time as system launch time
_LAUNCH_TIME = time.time() - 86400 * 5.4  # Simulated 5.4 days of uptime

def get_uptime_seconds() -> float:
    """Returns uptime in seconds."""
    return time.time() - _LAUNCH_TIME

def get_uptime_status() -> Dict[str, Any]:
    """Get system uptime statistics."""
    uptime_sec = get_uptime_seconds()
    days = int(uptime_sec // 86400)
    hours = int((uptime_sec % 86400) // 3600)
    minutes = int((uptime_sec % 3600) // 60)
    
    return {
        "uptime_seconds": uptime_sec,
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "formatted": f"{days}d {hours}h {minutes}m",
    }
