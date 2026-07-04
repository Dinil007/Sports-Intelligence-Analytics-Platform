"""System health aggregator."""
from __future__ import annotations

from typing import Dict, Any
from monitoring.constants import STATUS_HEALTHY, STATUS_WARNING, STATUS_CRITICAL
from monitoring.system.resource_monitor import get_cpu_status, get_memory_status, get_disk_status

def check_system_health() -> Dict[str, Any]:
    """Returns the aggregated health of the system."""
    cpu = get_cpu_status()
    memory = get_memory_status()
    disk = get_disk_status()
    
    statuses = [cpu["status"], memory["status"], disk["status"]]
    
    if STATUS_CRITICAL in statuses:
        overall = STATUS_CRITICAL
    elif STATUS_WARNING in statuses:
        overall = STATUS_WARNING
    else:
        overall = STATUS_HEALTHY
        
    return {
        "status": overall,
        "cpu": cpu,
        "memory": memory,
        "disk": disk,
    }
