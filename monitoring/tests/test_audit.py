"""Unit tests for audit activity log."""
from __future__ import annotations

import unittest
from monitoring.audit.audit_logger import fetch_audit_logs, log_audit_event
from monitoring.audit.audit_events import get_simulated_audit_events
from monitoring.audit.activity_history import get_activity_summary

class TestAuditMonitoring(unittest.TestCase):
    """Test cases for system activity audit trail."""
    
    def test_audit_logs(self) -> None:
        logs = fetch_audit_logs()
        self.assertTrue(len(logs) > 0)
        self.assertIn("user", logs[0])
        self.assertIn("action", logs[0])
        
    def test_log_event(self) -> None:
        self.assertTrue(log_audit_event("API Test", "test_user", "Success"))
        
    def test_summary_and_events(self) -> None:
        summary = get_activity_summary()
        self.assertEqual(summary["success_rate_percent"], 100.0)
        self.assertTrue(len(get_simulated_audit_events()) > 0)
