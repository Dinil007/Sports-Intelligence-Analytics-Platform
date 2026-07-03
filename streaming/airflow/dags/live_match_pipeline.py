"""Airflow DAG for live match event ingestion."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

# Try importing Airflow components; fallback to mock components if missing
try:
    from airflow import DAG # type: ignore
except ImportError:
    class DAG: # type: ignore
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass
        def __enter__(self) -> DAG:
            return self
        def __exit__(self, *args: Any) -> None:
            pass

from streaming.airflow.operators.match_operator import MatchOperator
from streaming.airflow.operators.validation_operator import ValidationOperator
from streaming.airflow.operators.load_operator import LoadOperator

default_args = {
    "owner": "sporta_data_ops",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

# Define DAG structure using context manager
with DAG(
    "live_match_pipeline",
    default_args=default_args,
    description="Real-time ingestion and processing of live match events",
    schedule_interval=None,  # Triggered manually or by match start webhook
    catchup=False,
) as dag:

    # 1. Extract raw live match events (e.g. for match 101)
    extract_live_events = MatchOperator(
        task_id="extract_live_events",
        match_id=101,
    )

    # 2. Validate and transform events
    validate_and_transform = ValidationOperator(
        task_id="validate_and_transform",
        input_task_id="extract_live_events",
    )

    # 3. Enrich and load to final destination
    enrich_and_load = LoadOperator(
        task_id="enrich_and_load",
        input_task_id="validate_and_transform",
    )

    # Define tasks dependency
    extract_live_events >> validate_and_transform >> enrich_and_load
