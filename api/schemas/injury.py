from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class InjuryResponse(BaseModel):
    risk: dict[str, Any] | list[dict[str, Any]] | None = None
    model_status: str | None = None