"""MLOps logging configuration."""

from __future__ import annotations

import logging
import sys

logger = logging.getLogger("mlops")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [MLOps] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
