from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class PlayerResponse(BaseModel):
    id: int | str | None = None
    name: str | None = None
    player_name: str | None = None
    club: str | None = None
    position: str | None = None
    age: float | None = None
    data: dict[str, Any] | None = None