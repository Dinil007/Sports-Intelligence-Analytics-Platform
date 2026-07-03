"""Airflow DAG for hourly incremental event processing."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

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
    "depends_on_past": True,
    "start_date": datetime(2026, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "incremental_pipeline",
    default_args=default_args,
    description="Hourly incremental ingestion and validation of match streams",
    schedule_interval="0 * * * *",  # Hourly
    catchup=False,
) as dag:

    # Incremental extract
    incremental_extract = MatchOperator(
        task_id="incremental_extract",
        match_id=102,
    )

    validate_incremental = ValidationOperator(
        task_id="validate_incremental",
        input_task_id="incremental_extract",
    )

    load_incremental = LoadOperator(
        task_id="load_incremental",
        input_task_id="validate_incremental",
    )

    incremental_extract >> validate_incremental >> load_incremental
