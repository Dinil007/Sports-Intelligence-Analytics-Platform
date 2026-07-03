from __future__ import annotations

from pydantic import BaseModel


class APISettings(BaseModel):
    title: str = "SPORTA VISTA PRO API"
    version: str = "1.0.0"
    description: str = "Enterprise Sports Intelligence REST API"
    allowed_origins: list[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8501",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8501",
    ]


settings = APISettings()