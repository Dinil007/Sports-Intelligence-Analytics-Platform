from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class TransferResponse(BaseModel):
    targets: list[dict[str, Any]] | None = None
    value: list[dict[str, Any]] | dict[str, Any] | None = None
    summary: list[str] | None = None