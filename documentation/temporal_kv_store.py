"""
Temporal Key-Value Store with Historical Versioning

This module provides a key-value store that maintains complete history of all
values, enabling time-travel queries to retrieve the state at any point in the past.

Features:
- O(log n) time-travel queries via binary search
- Soft delete (preserves audit trail) with optional hard delete
- Configurable timestamp precision (second/minute/hour)
- Full version history per key
"""

import bisect
import logging
from datetime import datetime
from enum import Enum
from typing import Any, Optional, List, Tuple

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TimestampPrecision(Enum):
    """Precision levels for timestamp normalization."""
    SECOND = "second"   # 2025-01-30 14:35:42
    MINUTE = "minute"   # 2025-01-30 14:35:00
    HOUR = "hour"       # 2025-01-30 14:00:00


class VersionedValue:
    """
    Represents a single version of a key's value.
    
    Immutable record containing:
    - timestamp: When this version was created
    - value: The actual value (None if deleted)
    - is_deleted: Whether this version represents a deletion
    """
    
    __slots__ = ('timestamp', 'value', 'is_deleted')
    
    def __init__(self, timestamp: datetime, value: Any, is_deleted: bool = False):
        self.timestamp = timestamp
        self.value = value
        self.is_deleted = is_deleted
    
    def __repr__(self) -> str:
        status = " (DELETED)" if self.is_deleted else ""
        return f"VersionedValue(ts={self.timestamp.isoformat()}, val={self.value!r}{status})"
    
    def __lt__(self, other) -> bool:
        """Enable sorting and bisect operations."""
        if isinstance(other, VersionedValue):
            return self.timestamp < other.timestamp
        # Allow comparison with raw datetime for bisect
        return self.timestamp < other
    
    def __le__(self, other) -> bool:
        if isinstance(other, VersionedValue):
            return self.timestamp <= other.timestamp
        return self.timestamp <= other
    
    def __eq__(self, other) -> bool:
        if isinstance(other, VersionedValue):
            return self.timestamp == other.timestamp
        # For bisect, only compare timestamps
        return self.timestamp == other
    
    def __gt__(self, other) -> bool:
        if isinstance(other, VersionedValue):
            return self.timestamp > other.timestamp
        return self.timestamp > other
    
    def __ge__(self, other) -> bool:
        if isinstance(other, VersionedValue):
            return self.timestamp >= other.timestamp
        return self.timestamp >= other


class TemporalKeyValueStore:
    """
    A key-value store with complete temporal history.
    
    Maintains all versions of each key's value, sorted by timestamp.
    Supports time-travel queries to retrieve values at any point in the past.
    
    Example:
        >>> store = TemporalKeyValueStore()
        >>> t1 = store.put("balance", 100)
        >>> time.sleep(1)
        >>> t2 = store.put("balance", 150)
        >>> store.get("balance")
        150
        >>> store.get_at_time("balance", t1)
        100
    """
    
    def __init__(self, precision: TimestampPrecision = TimestampPrecision.SECOND):
        """
        Initialize the temporal store.
        
        Args:
            precision: Timestamp precision for grouping updates
                      (SECOND, MINUTE, or HOUR)
        """
        self.store: dict[str, List[VersionedValue]] = {}
        self.precision = precision
    
    def _normalize_timestamp(self, timestamp: Optional[datetime] = None) -> datetime:
        """
        Round timestamp to configured precision level.
        
        Args:
            timestamp: Datetime to normalize (uses now() if None)
        
        Returns:
            Normalized datetime object with precision applied
        
        Examples:
            >>> store = TemporalKeyValueStore(TimestampPrecision.MINUTE)
            >>> ts = datetime(2025, 1, 30, 14, 35, 42, 123456)
            >>> normalized = store._normalize_timestamp(ts)
            >>> print(normalized)
            2025-01-30 14:35:00  # Seconds and microseconds zeroed
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        if self.precision == TimestampPrecision.MINUTE:
            timestamp = timestamp.replace(second=0, microsecond=0)
        elif self.precision == TimestampPrecision.SECOND:
            timestamp = timestamp.replace(microsecond=0)
        elif self.precision == TimestampPrecision.HOUR:
            timestamp = timestamp.replace(minute=0, second=0, microsecond=0)
        
        return timestamp
    
    def put(self, key: str, value: Any, timestamp: Optional[datetime] = None) -> datetime:
        """
        Insert or update a value at the given timestamp.
        
        If a version already exists at this timestamp, it's updated.
        Otherwise, a new version is inserted in sorted order.
        
        Args:
            key: The key to store
            value: The value to store
            timestamp: When to store this value (uses now() if None)
        
        Returns:
            The normalized timestamp when the value was stored
        
        Time Complexity: O(log n) + O(n) = O(n) worst case
                        (bisect_right is O(log n), list.insert is O(n))
        
        Example:
            >>> store = TemporalKeyValueStore()
            >>> t1 = store.put("user_age", 25)
            >>> store.put("user_age", 26)
            >>> store.get("user_age")
            26
        """
        timestamp = self._normalize_timestamp(timestamp)
        
        if key not in self.store:
            self.store[key] = [VersionedValue(timestamp, value)]
            logger.debug(f"Created new key '{key}' with value {value!r} at {timestamp}")
            return timestamp
        
        versions = self.store[key]
        
        # Find insertion point
        index = bisect.bisect_right(versions, timestamp, key=lambda v: v.timestamp)
        
        # Check if we should update the last version (same timestamp)
        if index > 0 and versions[index - 1].timestamp == timestamp:
            # Update existing version at this timestamp
            versions[index - 1] = VersionedValue(timestamp, value)
            logger.debug(f"Updated key '{key}' at {timestamp} to {value!r}")
        else:
            # Insert new version
            versions.insert(index, VersionedValue(timestamp, value))
            logger.debug(f"Inserted key '{key}' at {timestamp} with value {value!r}")
        
        return timestamp
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get the current value of a key.
        
        Returns the most recent non-deleted value, or None if the key
        doesn't exist or has been deleted.
        
        Args:
            key: The key to look up
        
        Returns:
            The current value, or None if not found/deleted
        
        Time Complexity: O(m) where m = number of versions
                        (iterates from end until finding non-deleted)
        
        Example:
            >>> store = TemporalKeyValueStore()
            >>> store.put("status", "active")
            >>> store.get("status")
            'active'
            >>> store.get("nonexistent")
            None
        """
        if key not in self.store:
            logger.debug(f"Key '{key}' not found in store")
            return None
        
        versions = self.store[key]
        
        # Iterate backwards to find the first non-deleted version
        for version in reversed(versions):
            if not version.is_deleted:
                return version.value
        
        # All versions are deleted
        return None
    
    def get_at_time(self, key: str, timestamp: Optional[datetime] = None) -> Optional[Any]:
        """
        Get the value of a key at a specific point in time.
        
        Performs a binary search to find the most recent version at or before
        the given timestamp. Returns None if the timestamp is before the first
        version or the value was deleted by that time.
        
        Args:
            key: The key to look up
            timestamp: The point in time to query (uses now() if None)
        
        Returns:
            The value at that time, or None if before first version/deleted
        
        Time Complexity: O(log n) binary search
        
        Example:
            >>> import time
            >>> store = TemporalKeyValueStore()
            >>> t1 = store.put("price", 10.00)
            >>> time.sleep(1)
            >>> t2 = store.put("price", 15.00)
            >>> store.get_at_time("price", t1)
            10.0
            >>> store.get_at_time("price", t2)
            15.0
        """
        if key not in self.store:
            logger.debug(f"Key '{key}' not found in store")
            return None
        
        if timestamp is None:
            return self.get(key)
        
        timestamp = self._normalize_timestamp(timestamp)
        versions = self.store[key]
        
        # Binary search: find the rightmost version at or before this timestamp
        # bisect_right returns the insertion point, so subtract 1
        index = bisect.bisect_right(versions, timestamp, key=lambda v: v.timestamp) - 1
        
        if index < 0:
            # Query time is before the first version
            logger.debug(f"Query time {timestamp} is before first version of '{key}'")
            return None
        
        version = versions[index]
        
        # Check if this version is deleted
        if version.is_deleted:
            return None
        
        return version.value
    
    def delete(self, key: str, timestamp: Optional[datetime] = None) -> bool:
        """
        Soft delete: mark a key as deleted at a specific timestamp.
        
        Creates a deletion marker that preserves the full history. The key
        is considered deleted from this point forward, but queries before
        this timestamp will still return the previous value.
        
        Use hard_delete() if you need to permanently erase all history
        (e.g., GDPR compliance).
        
        Args:
            key: The key to delete
            timestamp: When to mark as deleted (uses now() if None)
        
        Returns:
            True if deletion marker was added, False if key doesn't exist
        
        Time Complexity: O(log n) + O(n) for insertion
        
        Example:
            >>> import time
            >>> store = TemporalKeyValueStore()
            >>> t1 = store.put("secret", "password123")
            >>> time.sleep(1)
            >>> t2 = store.delete("secret")
            >>> store.get("secret")  # None - currently deleted
            None
            >>> store.get_at_time("secret", t1)  # But visible in past
            'password123'
        """
        if key not in self.store:
            logger.debug(f"Key '{key}' not found - cannot delete")
            return False
        
        timestamp = self._normalize_timestamp(timestamp)
        versions = self.store[key]
        
        # Insert deletion marker in sorted position
        deletion_marker = VersionedValue(timestamp, None, is_deleted=True)
        bisect.insort(versions, deletion_marker, key=lambda v: v.timestamp)
        
        logger.debug(f"Soft deleted key '{key}' at {timestamp}")
        return True
    
    def hard_delete(self, key: str) -> bool:
        """
        Permanently remove all history for a key.
        
        Completely erases all versions and history. Use for GDPR "right to
        be forgotten" or when removing sensitive PII. Once hard deleted,
        time-travel queries will not find the key.
        
        Args:
            key: The key to permanently delete
        
        Returns:
            True if deleted, False if key doesn't exist
        
        Time Complexity: O(1)
        
        Example:
            >>> store = TemporalKeyValueStore()
            >>> store.put("ssn", "123-45-6789")
            >>> store.hard_delete("ssn")  # Permanent erasure
            True
            >>> store.get("ssn")
            None
            >>> store.get_at_time("ssn", <any_timestamp>)
            None
        """
        if key in self.store:
            del self.store[key]
            logger.debug(f"Hard deleted key '{key}' - all history erased")
            return True
        return False
    
    def get_history(self, key: str) -> List[VersionedValue]:
        """
        Return all versions for a key in chronological order.
        
        Useful for auditing and understanding the complete history of a key.
        
        Args:
            key: The key to get history for
        
        Returns:
            List of VersionedValue objects, empty list if key doesn't exist
        
        Time Complexity: O(m) where m = number of versions
        
        Example:
            >>> store = TemporalKeyValueStore()
            >>> store.put("status", "pending")
            >>> store.put("status", "approved")
            >>> store.delete("status")
            >>> for v in store.get_history("status"):
            ...     print(f"{v.timestamp}: {v.value} (deleted={v.is_deleted})")
        """
        if key not in self.store:
            logger.debug(f"Key '{key}' not found - returning empty history")
            return []
        
        return self.store[key][:]  # Return a copy to prevent external modification
    
    def get_active_keys(self) -> List[str]:
        """
        Return all keys that currently exist and haven't been deleted.
        
        Args:
            None
        
        Returns:
            List of key names
        
        Time Complexity: O(n) where n = number of keys
                        (checks only the most recent version of each key)
        
        Example:
            >>> store = TemporalKeyValueStore()
            >>> store.put("user_1", "alice")
            >>> store.put("user_2", "bob")
            >>> store.delete("user_1")
            >>> store.get_active_keys()
            ['user_2']
        """
        active_keys = []
        
        for key, versions in self.store.items():
            # Check only the most recent version (last in sorted list)
            if versions:  # Safety check (should never be empty)
                most_recent = versions[-1]
                if not most_recent.is_deleted:
                    active_keys.append(key)
        
        return active_keys
    
    def size(self) -> int:
        """
        Return the total number of versions across all keys.
        
        Time Complexity: O(n * m)
        """
        return sum(len(versions) for versions in self.store.values())
    
    def num_keys(self) -> int:
        """Return the number of keys in the store (including deleted ones)."""
        return len(self.store)


# ==============================================================================
# DEMO AND TESTING
# ==============================================================================

def demo_basic_operations():
    """Demonstrate basic put/get/delete operations."""
    print("\n" + "="*70)
    print("DEMO: Basic Operations")
    print("="*70)
    
    store = TemporalKeyValueStore()
    
    # Put initial value
    t1 = store.put("balance", 100)
    print(f"[{t1}] Put balance=100")
    
    # Get current value
    current = store.get("balance")
    print(f"Current balance: {current}")
    
    # Verify exact query
    past = store.get_at_time("balance", t1)
    print(f"Balance at {t1}: {past}")


def demo_time_travel():
    """Demonstrate time-travel queries."""
    print("\n" + "="*70)
    print("DEMO: Time-Travel Queries")
    print("="*70)
    
    import time
    
    store = TemporalKeyValueStore()
    
    # Create multiple versions
    t1 = store.put("price", 10.00)
    print(f"[{t1}] Set price = 10.00")
    
    time.sleep(1)
    
    t2 = store.put("price", 15.00)
    print(f"[{t2}] Set price = 15.00")
    
    time.sleep(1)
    
    t3 = store.put("price", 20.00)
    print(f"[{t3}] Set price = 20.00")
    
    # Time-travel queries
    print(f"\nTime-travel queries:")
    print(f"  At {t1}: {store.get_at_time('price', t1)}")
    print(f"  At {t2}: {store.get_at_time('price', t2)}")
    print(f"  At {t3}: {store.get_at_time('price', t3)}")
    print(f"  Current: {store.get('price')}")


def demo_soft_delete():
    """Demonstrate soft delete with history preservation."""
    print("\n" + "="*70)
    print("DEMO: Soft Delete (Audit Trail)")
    print("="*70)
    
    import time
    
    store = TemporalKeyValueStore()
    
    # Create and delete
    t1 = store.put("secret", "password123")
    print(f"[{t1}] Created secret")
    
    time.sleep(1)
    
    t2 = store.delete("secret")
    print(f"[{t2}] Deleted secret")
    
    # Query current
    print(f"\nCurrent value: {store.get('secret')}")  # None
    
    # Query in the past (before deletion)
    print(f"Value at {t1}: {store.get_at_time('secret', t1)}")  # password123
    
    # Show full history
    print(f"\nFull history:")
    for v in store.get_history("secret"):
        print(f"  {v}")


def demo_precision():
    """Demonstrate timestamp precision effects."""
    print("\n" + "="*70)
    print("DEMO: Timestamp Precision (MINUTE precision)")
    print("="*70)
    
    import time
    
    store = TemporalKeyValueStore(precision=TimestampPrecision.MINUTE)
    
    # Multiple puts within same minute
    t1 = store.put("counter", 1)
    print(f"[{t1}] counter = 1")
    
    time.sleep(0.5)
    
    t2 = store.put("counter", 2)
    print(f"[{t2}] counter = 2")
    
    time.sleep(0.5)
    
    t3 = store.put("counter", 3)
    print(f"[{t3}] counter = 3")
    
    print(f"\nHistorical versions (should be 1, since all in same minute):")
    for v in store.get_history("counter"):
        print(f"  {v}")
    
    print(f"\nNote: t1={t1}, t2={t2}, t3={t3}")
    print(f"All normalized to same minute, so t1==t2==t3, updates replace previous")


if __name__ == "__main__":
    demo_basic_operations()
    demo_time_travel()
    demo_soft_delete()
    demo_precision()
    
    print("\n" + "="*70)
    print("All demos completed!")
    print("="*70)
