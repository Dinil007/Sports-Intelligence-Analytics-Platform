from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class TeamResponse(BaseModel):
    id: int | str | None = None
    name: str
    ranking: int | None = None
    metrics: dict[str, Any] | None = None