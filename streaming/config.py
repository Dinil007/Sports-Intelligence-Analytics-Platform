"""Configuration manager for the Streaming Platform."""

from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class StreamingConfig:
    """Config settings for real-time football event streaming and Airflow execution."""
    
    # Kafka broker config
    BOOTSTRAP_SERVERS: list[str] = [
        s.strip() for s in os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092").split(",")
    ]
    CLIENT_ID: str = os.getenv("KAFKA_CLIENT_ID", "sporta-streaming-client")
    GROUP_ID: str = os.getenv("KAFKA_GROUP_ID", "sporta-analytics-group")
    
    # Producer reliability
    ACKS: str = os.getenv("KAFKA_ACKS", "all")
    RETRIES: int = int(os.getenv("KAFKA_RETRIES", "5"))
    RETRY_BACKOFF_MS: int = int(os.getenv("KAFKA_RETRY_BACKOFF_MS", "100"))
    
    # Batch/Linger settings
    BATCH_SIZE: int = int(os.getenv("KAFKA_BATCH_SIZE", "16384"))  # 16KB
    LINGER_MS: int = int(os.getenv("KAFKA_LINGER_MS", "10"))
    
    # Pipeline properties
    ENRICH_WITH_DATABASE: bool = os.getenv("PIPELINE_ENRICH_DB", "True").lower() == "true"
    METRICS_PUBLISH_INTERVAL_SEC: int = int(os.getenv("PIPELINE_METRICS_INTERVAL", "15"))

    # Airflow configuration
    AIRFLOW_DAG_DIR: Path = Path(os.getenv("AIRFLOW_DAG_DIR", "/usr/local/airflow/dags"))
    
    # Simulated connection mode (useful if Kafka is not running)
    SIMULATE_BROKER: bool = os.getenv("STREAMING_SIMULATE_BROKER", "True").lower() == "true"

config = StreamingConfig()
