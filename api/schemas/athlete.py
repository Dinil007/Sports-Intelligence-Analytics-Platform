from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class AthleteResponse(BaseModel):
    workload: dict[str, Any] | None = None
    fatigue: dict[str, Any] | None = None
    recovery: dict[str, Any] | None = None
    summary: list[str] | None = None