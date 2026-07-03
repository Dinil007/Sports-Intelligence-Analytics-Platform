from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def success_response(message: str, data: Any = None) -> dict[str, Any]:
    return {"status": "success", "message": message, "data": data, "timestamp": utc_timestamp()}


def error_response(message: str, data: Any = None, status: str = "error") -> dict[str, Any]:
    return {"status": status, "message": message, "data": data, "timestamp": utc_timestamp()}