"""ETL data pipeline overall status."""
from __future__ import annotations

from typing import List, Dict, Any

def get_pipelines_status() -> List[Dict[str, Any]]:
    """Return status of all registered data integration pipelines."""
    return [
        {"pipeline": "Core ETL Sync", "success_rate_percent": 100.0, "status": "Idle", "last_run_at": "2026-07-04T12:00:00Z"},
        {"pipeline": "Scouting ETL Sync", "success_rate_percent": 100.0, "status": "Idle", "last_run_at": "2026-07-04T13:00:00Z"},
    ]
