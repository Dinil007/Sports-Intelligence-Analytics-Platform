"""Unit tests for database monitoring."""
from __future__ import annotations

import unittest
from monitoring.database.database_monitor import check_database_health
from monitoring.database.connection_monitor import get_active_connections, get_connection_history
from monitoring.database.query_monitor import get_slow_queries
from monitoring.database.storage_monitor import get_db_size_gb

class TestDatabaseMonitoring(unittest.TestCase):
    """Test cases for database performance and connections."""
    
    def test_database_health(self) -> None:
        health = check_database_health()
        self.assertEqual(health["status"], "Healthy")
        
    def test_connections(self) -> None:
        active = get_active_connections()
        self.assertTrue(active > 0)
        history = get_connection_history()
        self.assertEqual(len(history), 12)
        
    def test_queries_and_storage(self) -> None:
        slow = get_slow_queries()
        self.assertTrue(len(slow) > 0)
        self.assertTrue(get_db_size_gb() > 0)
        
if __name__ == "__main__":
    unittest.main()
