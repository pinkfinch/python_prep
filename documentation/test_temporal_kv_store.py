"""
Comprehensive test suite for Temporal Key-Value Store.
Uses explicit timestamps to avoid precision rounding during fast test execution.
"""

import unittest
import time
from datetime import datetime, timedelta
from temporal_kv_store import (
    TemporalKeyValueStore,
    VersionedValue,
    TimestampPrecision
)


class TestVersionedValue(unittest.TestCase):
    """Test the VersionedValue class."""
    
    def test_versioned_value_creation(self):
        """Test creating a VersionedValue."""
        ts = datetime.now()
        v = VersionedValue(ts, "test_value")
        
        self.assertEqual(v.timestamp, ts)
        self.assertEqual(v.value, "test_value")
        self.assertFalse(v.is_deleted)
    
    def test_comparison_operators(self):
        """Test that comparison operators work for bisect."""
        ts1 = datetime(2025, 1, 30, 10, 0, 0)
        ts2 = datetime(2025, 1, 30, 10, 1, 0)
        
        v1 = VersionedValue(ts1, "first")
        v2 = VersionedValue(ts2, "second")
        
        self.assertTrue(v1 < v2)
        self.assertTrue(v1 <= v2)
        self.assertTrue(v2 > v1)
        self.assertTrue(v2 >= v1)


class TestBasicOperations(unittest.TestCase):
    """Test basic put/get/delete operations."""
    
    def setUp(self):
        """Create a fresh store for each test."""
        self.store = TemporalKeyValueStore()
    
    def test_put_and_get_single_key(self):
        """Test putting and getting a single value."""
        self.store.put("name", "Alice")
        self.assertEqual(self.store.get("name"), "Alice")
    
    def test_get_nonexistent_key(self):
        """Test getting a key that doesn't exist."""
        self.assertIsNone(self.store.get("nonexistent"))
    
    def test_put_various_value_types(self):
        """Test storing different value types."""
        self.store.put("int", 42)
        self.store.put("float", 3.14)
        self.store.put("str", "hello")
        self.store.put("list", [1, 2, 3])
        
        self.assertEqual(self.store.get("int"), 42)
        self.assertEqual(self.store.get("float"), 3.14)
        self.assertEqual(self.store.get("str"), "hello")
        self.assertEqual(self.store.get("list"), [1, 2, 3])


class TestTemporalQueries(unittest.TestCase):
    """Test time-travel query functionality."""
    
    def setUp(self):
        """Create a store with multiple versions using explicit timestamps."""
        self.store = TemporalKeyValueStore()
        
        # Use explicit timestamps to avoid precision rounding
        self.ts1 = datetime(2025, 1, 30, 10, 0, 0)
        self.ts2 = datetime(2025, 1, 30, 10, 0, 1)
        self.ts3 = datetime(2025, 1, 30, 10, 0, 2)
        
        self.store.put("balance", 100, self.ts1)
        self.store.put("balance", 150, self.ts2)
        self.store.put("balance", 200, self.ts3)
    
    def test_get_at_exact_timestamp(self):
        """Test querying at exact timestamp."""
        self.assertEqual(self.store.get_at_time("balance", self.ts1), 100)
        self.assertEqual(self.store.get_at_time("balance", self.ts2), 150)
        self.assertEqual(self.store.get_at_time("balance", self.ts3), 200)
    
    def test_get_at_time_between_versions(self):
        """Test querying between two versions returns earlier version."""
        between = self.ts1 + timedelta(seconds=0.5)
        self.assertEqual(self.store.get_at_time("balance", between), 100)
        
        between = self.ts2 + timedelta(seconds=0.5)
        self.assertEqual(self.store.get_at_time("balance", between), 150)
    
    def test_get_at_time_before_first_version(self):
        """Test querying before first version returns None."""
        before = self.ts1 - timedelta(seconds=1)
        self.assertIsNone(self.store.get_at_time("balance", before))
    
    def test_get_at_time_after_all_versions(self):
        """Test querying after all versions returns current value."""
        after = self.ts3 + timedelta(seconds=1)
        self.assertEqual(self.store.get_at_time("balance", after), 200)


class TestSoftDelete(unittest.TestCase):
    """Test soft delete behavior."""
    
    def setUp(self):
        """Create a store with delete history using explicit timestamps."""
        self.store = TemporalKeyValueStore()
        
        self.ts1 = datetime(2025, 1, 30, 10, 0, 0)
        self.ts2 = datetime(2025, 1, 30, 10, 0, 1)
        self.ts3 = datetime(2025, 1, 30, 10, 0, 2)
        
        self.store.put("secret", "password123", self.ts1)
        self.store.delete("secret", self.ts2)
        self.store.put("secret", "newpassword", self.ts3)
    
    def test_query_before_delete(self):
        """Test that querying before delete returns the value."""
        self.assertEqual(self.store.get_at_time("secret", self.ts1), "password123")
    
    def test_query_after_delete_before_restore(self):
        """Test that query after delete returns None."""
        between = self.ts2 + timedelta(seconds=0.5)
        self.assertIsNone(self.store.get_at_time("secret", between))
    
    def test_query_after_restore(self):
        """Test that query after restore returns new value."""
        self.assertEqual(self.store.get_at_time("secret", self.ts3), "newpassword")
    
    def test_soft_delete_creates_marker(self):
        """Test that soft delete creates deletion marker."""
        history = self.store.get_history("secret")
        # Should have: original, delete marker, restored
        self.assertEqual(len(history), 3)
        self.assertTrue(history[1].is_deleted)


class TestTimestampPrecision(unittest.TestCase):
    """Test timestamp precision settings."""
    
    def test_minute_precision_groups_same_minute(self):
        """Test MINUTE precision groups updates within same minute."""
        store = TemporalKeyValueStore(precision=TimestampPrecision.MINUTE)
        
        ts1 = datetime(2025, 1, 30, 10, 0, 30)
        ts2 = datetime(2025, 1, 30, 10, 0, 45)
        
        store.put("counter", 1, ts1)
        store.put("counter", 2, ts2)
        
        # Both normalize to same minute, last value wins
        history = store.get_history("counter")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].value, 2)
    
    def test_minute_precision_separates_different_minutes(self):
        """Test MINUTE precision separates different minutes."""
        store = TemporalKeyValueStore(precision=TimestampPrecision.MINUTE)
        
        ts1 = datetime(2025, 1, 30, 10, 0, 45)
        ts2 = datetime(2025, 1, 30, 10, 1, 30)
        
        store.put("value", "first", ts1)
        store.put("value", "second", ts2)
        
        history = store.get_history("value")
        self.assertEqual(len(history), 2)


class TestHistory(unittest.TestCase):
    """Test version history tracking."""
    
    def test_get_history_empty(self):
        """Test getting history of nonexistent key."""
        store = TemporalKeyValueStore()
        history = store.get_history("nonexistent")
        self.assertEqual(history, [])
    
    def test_history_is_sorted_chronologically(self):
        """Test that history is in chronological order."""
        store = TemporalKeyValueStore()
        
        ts1 = datetime(2025, 1, 30, 10, 0, 0)
        ts2 = datetime(2025, 1, 30, 10, 0, 1)
        ts3 = datetime(2025, 1, 30, 10, 0, 2)
        
        store.put("value", "first", ts1)
        store.put("value", "second", ts2)
        store.put("value", "third", ts3)
        
        history = store.get_history("value")
        
        self.assertTrue(history[0].timestamp <= history[1].timestamp)
        self.assertTrue(history[1].timestamp <= history[2].timestamp)


class TestActiveKeys(unittest.TestCase):
    """Test getting list of active (non-deleted) keys."""
    
    def test_get_active_keys_all_active(self):
        """Test getting active keys when all are active."""
        store = TemporalKeyValueStore()
        
        store.put("key1", "value1")
        store.put("key2", "value2")
        store.put("key3", "value3")
        
        active = store.get_active_keys()
        self.assertEqual(set(active), {"key1", "key2", "key3"})
    
    def test_get_active_keys_with_deleted(self):
        """Test that deleted keys are excluded."""
        store = TemporalKeyValueStore()
        
        ts1 = datetime(2025, 1, 30, 10, 0, 0)
        ts2 = datetime(2025, 1, 30, 10, 0, 1)
        
        store.put("active", "yes", ts1)
        store.put("deleted", "no", ts1)
        store.delete("deleted", ts2)
        
        active = store.get_active_keys()
        self.assertEqual(active, ["active"])


class TestHardDelete(unittest.TestCase):
    """Test hard delete (permanent removal)."""
    
    def test_hard_delete_removes_all_history(self):
        """Test that hard delete removes all versions."""
        store = TemporalKeyValueStore()
        
        ts = datetime(2025, 1, 30, 10, 0, 0)
        store.put("secret", "value", ts)
        store.hard_delete("secret")
        
        self.assertIsNone(store.get("secret"))
        self.assertEqual(store.get_history("secret"), [])
    
    def test_hard_delete_breaks_time_travel(self):
        """Test that hard deleted keys cannot be queried in past."""
        store = TemporalKeyValueStore()
        
        ts = datetime(2025, 1, 30, 10, 0, 0)
        store.put("secret", "value", ts)
        store.hard_delete("secret")
        
        # Query in the past should return None
        self.assertIsNone(store.get_at_time("secret", ts))


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_same_timestamp_updates_previous_version(self):
        """Test that putting at same timestamp updates the version."""
        store = TemporalKeyValueStore()
        
        ts = datetime(2025, 1, 30, 10, 0, 0)
        store.put("key", "value1", ts)
        store.put("key", "value2", ts)
        
        # Should only have one version
        history = store.get_history("key")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].value, "value2")
    
    def test_empty_string_value(self):
        """Test storing empty string."""
        store = TemporalKeyValueStore()
        store.put("empty", "")
        self.assertEqual(store.get("empty"), "")
    
    def test_zero_value(self):
        """Test storing zero."""
        store = TemporalKeyValueStore()
        store.put("zero", 0)
        self.assertEqual(store.get("zero"), 0)


class TestStoreMetrics(unittest.TestCase):
    """Test store metrics and introspection."""
    
    def test_size_returns_total_versions(self):
        """Test that size() returns total number of versions."""
        store = TemporalKeyValueStore()
        
        ts1 = datetime(2025, 1, 30, 10, 0, 0)
        ts2 = datetime(2025, 1, 30, 10, 0, 1)
        
        store.put("k1", "v1", ts1)
        store.put("k1", "v2", ts2)
        store.put("k2", "v1", ts1)
        
        # 3 total versions
        self.assertEqual(store.size(), 3)
    
    def test_num_keys_returns_unique_keys(self):
        """Test that num_keys() returns number of unique keys."""
        store = TemporalKeyValueStore()
        
        ts1 = datetime(2025, 1, 30, 10, 0, 0)
        
        store.put("k1", "v1", ts1)
        store.put("k1", "v2", ts1)
        store.put("k2", "v1", ts1)
        
        # 2 unique keys
        self.assertEqual(store.num_keys(), 2)


if __name__ == "__main__":
    unittest.main()
