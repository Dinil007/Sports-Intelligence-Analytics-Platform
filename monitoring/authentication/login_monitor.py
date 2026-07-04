"""Login statistics and auditing."""
from __future__ import annotations

from typing import List, Dict, Any

def get_login_statistics() -> Dict[str, Any]:
    """Return simulated login statistics."""
    return {
        "logins_24h": 48,
        "failed_attempts_24h": 2,
        "unique_users_24h": 12,
    }

def get_login_trends() -> List[Dict[str, Any]]:
    """Return historical logins for Line chart."""
    logins = [2, 1, 0, 4, 8, 12, 10, 6, 3, 1, 0, 1]
    history = []
    for i, val in enumerate(logins):
        history.append({
            "hour": f"-{12-i}h",
            "logins": val
        })
    return history
