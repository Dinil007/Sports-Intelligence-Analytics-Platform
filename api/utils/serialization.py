from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any


def serialize(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): serialize(item) for key, item in value.items()}
    if isinstance(value, list | tuple | set):
        return [serialize(item) for item in value]
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    return value