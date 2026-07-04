"""Unit tests for ETL pipeline monitoring."""
from __future__ import annotations

import unittest
from monitoring.etl.etl_monitor import check_etl_health
from monitoring.etl.job_monitor import get_recent_job_runs
from monitoring.etl.pipeline_monitor import get_pipelines_status
from monitoring.etl.scheduler_monitor import get_scheduler_status

class TestEtlMonitoring(unittest.TestCase):
    """Test cases for ETL processing pipelines."""
    
    def test_etl_health(self) -> None:
        health = check_etl_health()
        self.assertEqual(health["status"], "Healthy")
        self.assertEqual(health["success_rate_percent"], 100.0)
        
    def test_jobs(self) -> None:
        jobs = get_recent_job_runs()
        self.assertTrue(len(jobs) > 0)
        self.assertEqual(jobs[0]["status"], "Success")
        
    def test_pipelines_and_scheduler(self) -> None:
        self.assertTrue(len(get_pipelines_status()) > 0)
        self.assertEqual(get_scheduler_status()["status"], "Active")
