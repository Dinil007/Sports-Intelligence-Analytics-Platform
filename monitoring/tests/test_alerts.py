"""Unit tests for Alert Rules Engine."""
from __future__ import annotations

import unittest
from monitoring.alerts.alert_engine import run_alert_rules
from monitoring.alerts.alert_manager import get_active_alerts
from monitoring.alerts.alert_rules import get_alert_thresholds
from monitoring.alerts.notification_manager import dispatch_notification

class TestAlertsMonitoring(unittest.TestCase):
    """Test cases for alerting conditions and alert levels."""
    
    def test_alert_rules(self) -> None:
        alerts = run_alert_rules()
        self.assertTrue(len(alerts) > 0)
        self.assertIn("level", alerts[0])
        
    def test_active_alerts(self) -> None:
        active = get_active_alerts()
        self.assertTrue(len(active) > 0)
        
    def test_thresholds_and_notifications(self) -> None:
        thresholds = get_alert_thresholds()
        self.assertIn("cpu_warning", thresholds)
        self.assertTrue(dispatch_notification({"test": "alert"}))
