from __future__ import annotations

import logging
from time import perf_counter
from typing import Any

from fastapi import Request


logger = logging.getLogger("sporta_vista_api")


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")


def request_context(request: Request) -> dict[str, Any]:
    return {"method": request.method, "path": request.url.path, "client": request.client.host if request.client else None}


def timer_start() -> float:
    return perf_counter()


def elapsed_ms(start: float) -> float:
    return round((perf_counter() - start) * 1000, 2)