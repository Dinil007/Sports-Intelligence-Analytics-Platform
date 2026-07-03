"""Enterprise logging configuration for the Streaming Platform."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

# Create log directory inside streaming
LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "streaming.log"

def setup_logging(name: str = "streaming") -> logging.Logger:
    """Configure and return a structured logger for the streaming application."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d]: %(message)s"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler
    try:
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Failed to initialize file logger: {e}", file=sys.stderr)

    return logger

logger = setup_logging()
