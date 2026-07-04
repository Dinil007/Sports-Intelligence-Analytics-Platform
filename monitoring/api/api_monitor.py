"""API health status and aggregation."""
from __future__ import annotations

from typing import Dict, Any
from monitoring.api.request_monitor import get_request_volume
from monitoring.api.response_monitor import get_error_rate, get_p95_latency
from monitoring.api.endpoint_statistics import get_top_endpoints
from monitoring.constants import STATUS_HEALTHY, STATUS_WARNING

def check_api_health() -> Dict[str, Any]:
    """Calculate aggregate API health metric."""
    err_rate = get_error_rate()
    p95_lat = get_p95_latency()
    
    if err_rate > 2.0 or p95_lat > 200:
        status = STATUS_WARNING
    else:
        status = STATUS_HEALTHY
        
    return {
        "status": status,
        "request_volume": get_request_volume(),
        "error_rate_percent": err_rate,
        "p95_latency_ms": p95_lat,
        "top_endpoints": get_top_endpoints(),
    }
