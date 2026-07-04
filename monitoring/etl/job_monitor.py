"""Individual ETL job run monitoring."""
from __future__ import annotations

from typing import List, Dict, Any

def get_recent_job_runs() -> List[Dict[str, Any]]:
    """Return logs of individual job runs."""
    return [
        {"job_name": "matches_sync", "status": "Success", "records_processed": 120, "elapsed_seconds": 15},
        {"job_name": "player_stats_agg", "status": "Success", "records_processed": 850, "elapsed_seconds": 84},
        {"job_name": "scouting_sync", "status": "Success", "records_processed": 45, "elapsed_seconds": 8},
    ]
