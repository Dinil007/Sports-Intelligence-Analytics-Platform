"""Airflow DAG for daily bulk database sync and event refresh."""

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
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=10),
}

with DAG(
    "daily_refresh_pipeline",
    default_args=default_args,
    description="Daily bulk synchronization and validation of historical events",
    schedule_interval="30 2 * * *",  # Daily at 2:30 AM
    catchup=False,
) as dag:

    daily_bulk_extract = MatchOperator(
        task_id="daily_bulk_extract",
        match_id=103,
    )

    validate_daily_bulk = ValidationOperator(
        task_id="validate_daily_bulk",
        input_task_id="daily_bulk_extract",
    )

    load_daily_bulk = LoadOperator(
        task_id="load_daily_bulk",
        input_task_id="validate_daily_bulk",
    )

    daily_bulk_extract >> validate_daily_bulk >> load_daily_bulk
