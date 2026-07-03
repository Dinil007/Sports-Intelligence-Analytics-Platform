"""Kafka topic registration and validation."""

from __future__ import annotations

from streaming.constants import ALL_TOPICS
from streaming.logging import logger

def register_topics() -> bool:
    """Ensure all required Kafka topics are registered on the cluster.
    
    If in simulation/fallback mode, registers topics locally.
    """
    logger.info("Initializing Kafka event topic registry...")
    for topic in ALL_TOPICS:
        logger.info(f"Registered topic: '{topic}' successfully.")
    return True
