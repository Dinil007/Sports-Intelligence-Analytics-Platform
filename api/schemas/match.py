from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class MatchResponse(BaseModel):
    id: int | str | None = None
    home_team: str | None = None
    away_team: str | None = None
    date: str | None = None
    data: dict[str, Any] | None = None