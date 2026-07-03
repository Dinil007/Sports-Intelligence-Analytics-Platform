from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ScoutingResponse(BaseModel):
    players: list[dict[str, Any]] | None = None
    profile: dict[str, Any] | None = None
    summary: str | list[str] | None = None