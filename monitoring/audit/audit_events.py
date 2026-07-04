"""Audit log simulated event log definition."""
from __future__ import annotations

from typing import List, Dict, Any

def get_simulated_audit_events() -> List[Dict[str, Any]]:
    """Return simulated system activity log entries."""
    return [
        {
            "timestamp": "2026-07-04T14:52:10Z",
            "user": "admin",
            "action": "User Login",
            "status": "Success",
            "ip_address": "192.168.1.42"
        },
        {
            "timestamp": "2026-07-04T14:48:32Z",
            "user": "system",
            "action": "Prediction Executed",
            "status": "Success",
            "ip_address": "127.0.0.1"
        },
        {
            "timestamp": "2026-07-04T14:42:15Z",
            "user": "analyst",
            "action": "Model Registered",
            "status": "Success",
            "ip_address": "192.168.1.105"
        },
        {
            "timestamp": "2026-07-04T14:35:00Z",
            "user": "admin",
            "action": "Model Promoted",
            "status": "Success",
            "ip_address": "192.168.1.42"
        },
        {
            "timestamp": "2026-07-04T14:15:00Z",
            "user": "system",
            "action": "Pipeline Started",
            "status": "Success",
            "ip_address": "127.0.0.1"
        },
        {
            "timestamp": "2026-07-04T14:19:45Z",
            "user": "system",
            "action": "Pipeline Completed",
            "status": "Success",
            "ip_address": "127.0.0.1"
        },
        {
            "timestamp": "2026-07-04T14:05:00Z",
            "user": "analyst",
            "action": "API Request",
            "status": "Success",
            "ip_address": "192.168.1.105"
        },
        {
            "timestamp": "2026-07-04T13:30:00Z",
            "user": "system",
            "action": "Database Backup",
            "status": "Success",
            "ip_address": "127.0.0.1"
        },
        {
            "timestamp": "2026-07-04T13:00:00Z",
            "user": "system",
            "action": "Streaming Started",
            "status": "Success",
            "ip_address": "127.0.0.1"
        }
    ]
