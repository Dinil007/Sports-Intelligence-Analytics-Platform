"""Unit tests for system monitoring."""
from __future__ import annotations

import unittest
from monitoring.system.system_health import check_system_health
from monitoring.system.resource_monitor import get_cpu_status, get_memory_status
from monitoring.system.uptime_monitor import get_uptime_status
from monitoring.system.service_status import check_services_status

class TestSystemMonitoring(unittest.TestCase):
    """Test cases for host system metrics."""
    
    def test_overall_health(self) -> None:
        health = check_system_health()
        self.assertIn("status", health)
        self.assertIn("cpu", health)
        self.assertIn("memory", health)
        
    def test_resource_monitor(self) -> None:
        cpu = get_cpu_status()
        self.assertTrue(0.0 <= cpu["percentage"] <= 100.0)
        self.assertIn("status", cpu)
        
        mem = get_memory_status()
        self.assertTrue(0.0 <= mem["percentage"] <= 100.0)
        
    def test_uptime(self) -> None:
        uptime = get_uptime_status()
        self.assertIn("formatted", uptime)
        self.assertTrue(uptime["uptime_seconds"] > 0)
        
    def test_services(self) -> None:
        services = check_services_status()
        self.assertTrue(len(services) > 0)
        self.assertEqual(services[0]["status"], "Healthy")
