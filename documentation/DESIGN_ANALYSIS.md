# Temporal Key-Value Store: Analysis & Design Recommendations

## Executive Summary

Your implementation has the right idea—tracking historical values per key using timestamps and binary search—but contains critical bugs in the `get_effective_date()` method and the `delete()` method. This document analyzes the issues and recommends design patterns for production use.

---

## Critical Bugs Identified

### Bug 1: Incorrect Binary Search Logic in `get_effective_date()`

**Current Code:**
```python
left = bisect.bisect_left(inner, timestamp, key=lambda i:i[0])
if left == 0:
    return None
if left < len(inner):
    if inner[left] == timestamp or (left + 1 < len(inner) and timestamp < inner[left+1][0]):
        return inner[left][1]
return None
```

**Problem:** `bisect_left()` returns the insertion point for the timestamp to maintain sorted order. If you want the value *at or before* a given timestamp, you need `bisect_right()` minus 1.

**Example:**
- Versions at timestamps: [10:00, 10:01, 10:02]
- Query at: 10:01:30
- `bisect_left()` returns index 2 (where 10:01:30 would insert)
- But you want index 1 (the 10:01 value)
- `bisect_right()` returns index 2, then subtract 1 → index 1 ✓

**Fix:**
```python
def get_effective_date(self, key, timestamp):
    if key not in self.store:
        logging.debug("Invalid key passed in")
        return None
    
    if timestamp is None:
        return self.get(key)
    
    inner = self.store[key]
    # bisect_right returns insertion point; subtract 1 for last version before timestamp
    index = bisect.bisect_right(inner, timestamp, key=lambda i: i[0]) - 1
    
    if index < 0:
        return None  # Query time is before first version
    
    return inner[index][1]
```

---

### Bug 2: Invalid `delete()` Method Call

**Current Code:**
```python
def delete(self, key, timestamp):
    if key in self.store:
        timestamp_list = self.store[key]
        timestamp = timestamp.strftime(DataStore.date_format)
        index = bisect.bisect_left(timestamp_list, timestamp, key=lambda i:i[0])
        if timestamp_list[index][0] == timestamp:
            timestamp_list.remove(index)  # ❌ WRONG
```

**Problem:** `list.remove()` removes by *value*, not by index. You're passing an integer index, which will fail if the value `index` doesn't exist in the list. The correct method is `pop()`.

**Fix:**
```python
timestamp_list.pop(index)  # ✓ Removes element at index
```

---

### Bug 3: Inconsistent Timestamp Handling

**Problem:** You convert datetime to string in `put()` but accept datetime objects in `delete()`, then convert again. This creates:
1. String formatting inconsistencies
2. Microsecond precision loss
3. Ambiguity in comparisons

**Better Approach:** Keep timestamps as `datetime` objects internally, format only for display.

---

## Design Decision: Tuple vs Class

### Question
Should you use tuples `(timestamp, value)` or a class `VersionedValue(timestamp, value)`?

### Answer: Use a Class

**Tuple Approach:**
```python
inner = [(timestamp, value), (timestamp, value)]
# Later:
inner[0][1]  # What does this mean? Only works if you remember the order
```

**Class Approach:**
```python
class VersionedValue:
    def __init__(self, timestamp, value):
        self.timestamp = timestamp
        self.value = value

inner = [VersionedValue(ts, val), VersionedValue(ts, val)]
# Later:
inner[0].value  # Clear and self-documenting
```

**Advantages of Class:**
1. **Explicit field names** – `version.timestamp` vs `version[0]` (what is [0]?)
2. **Type safety** – IDE autocomplete, mypy static checking
3. **Extensibility** – Easy to add `user`, `reason`, `operation_id` fields later
4. **Custom methods** – Can add validation, comparison operators for bisect
5. **Better debugging** – Custom `__repr__` shows all fields

**Disadvantages:**
- ~16 bytes per instance overhead (negligible at scale)
- Slight mental overhead when learning code

**Memory Comparison:**
- Tuple: ~56 bytes per `(datetime, str)`
- Class: ~72 bytes (16 bytes overhead)
- **Trade-off:** Worth the 30% overhead for massive readability gain

---

## Design Decision: Timestamp Precision

### Problem
Storing every put at nanosecond precision leads to millions of versions for high-frequency updates. Do you need second-level granularity, or can you round to minutes?

### Solution: Configurable Precision

```python
from enum import Enum

class TimestampPrecision(Enum):
    SECOND = "second"   # 2025-01-30 14:35:42
    MINUTE = "minute"   # 2025-01-30 14:35:00
    HOUR = "hour"       # 2025-01-30 14:00:00

class TemporalKeyValueStore:
    def __init__(self, precision=TimestampPrecision.SECOND):
        self.precision = precision
        self.store = {}
    
    def _normalize_timestamp(self, timestamp=None):
        """Round timestamp to configured precision."""
        if timestamp is None:
            timestamp = datetime.now()
        
        if self.precision == TimestampPrecision.MINUTE:
            timestamp = timestamp.replace(second=0, microsecond=0)
        elif self.precision == TimestampPrecision.SECOND:
            timestamp = timestamp.replace(microsecond=0)
        # HOUR would drop seconds too
        
        return timestamp
```

**Trade-offs:**
- **SECOND:** Captures every update, larger storage, slower queries
- **MINUTE:** Groups updates within same minute, 60× fewer versions, acceptable for most applications
- **HOUR:** Groups by hour, minimal storage, but loses intra-minute resolution

**Use Cases:**
- Real-time metrics → SECOND
- Event logs → MINUTE
- Billing/analytics → HOUR

---

## Design Decision: Soft Delete vs Hard Delete

### Soft Delete (Default)

Store a "delete marker" instead of removing the version:

```python
class VersionedValue:
    def __init__(self, timestamp, value, is_deleted=False):
        self.timestamp = timestamp
        self.value = value
        self.is_deleted = is_deleted

def delete(self, key, timestamp):
    """Mark value as deleted at timestamp."""
    timestamp = self._normalize_timestamp(timestamp)
    versions = self.store[key]
    index = bisect.bisect_right(versions, timestamp, key=lambda v: v.timestamp) - 1
    
    if index >= 0:
        # Insert deletion marker
        versions.insert(index + 1, VersionedValue(timestamp, None, is_deleted=True))
```

**Advantages:**
- Preserves full audit trail
- Time-travel queries work correctly (query before deletion returns old value)
- Can undelete by querying historical state
- Compliance requirements (HIPAA, SOX) often require immutable deletion records

**Example:**
```
Key: "user_balance"
Versions:
  10:00 → $100
  10:05 → $150
  10:10 → DELETED
  10:15 → $200 (undelete)

Query at 10:00 → $100 ✓
Query at 10:08 → $150 ✓
Query at 10:12 → null ✓ (marked deleted)
```

### Hard Delete (Optional)

Completely remove all history:

```python
def hard_delete(self, key):
    """Permanently remove all history for a key."""
    if key in self.store:
        del self.store[key]
```

**Use Cases:**
- GDPR "right to be forgotten"
- Removing sensitive PII
- Cleanup of test data

---

## Performance Analysis

### Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| `put()` | O(log n) + O(n) | bisect_right O(log n), list.insert O(n) worst case |
| `get()` | O(1) | Access last version directly |
| `get_at_time()` | O(log n) | Binary search only |
| `delete()` | O(log n) + O(n) | Same as put |
| `get_history()` | O(m) | m = number of versions for key |

### Space Complexity

- **Per key:** O(m) where m = number of versions
- **Total:** O(n × m) where n = number of keys, m = average versions per key
- With MINUTE precision, m is reduced 60× vs microsecond precision

### Optimization Tips

1. **For high-frequency updates:** Use MINUTE or HOUR precision
2. **For large key spaces:** Consider sharding by key prefix
3. **For old data:** Archive old versions to cold storage (S3, database)
4. **For indexing:** Add reverse index for get_keys_modified_after(timestamp)

---

## Recommended Implementation Pattern

```python
from enum import Enum
from datetime import datetime
import bisect
import logging

logging.basicConfig(level=logging.DEBUG)

class TimestampPrecision(Enum):
    SECOND = "second"
    MINUTE = "minute"

class VersionedValue:
    """Immutable version record."""
    
    def __init__(self, timestamp, value, is_deleted=False):
        self.timestamp = timestamp
        self.value = value
        self.is_deleted = is_deleted
    
    def __repr__(self):
        status = " (DELETED)" if self.is_deleted else ""
        return f"VersionedValue({self.timestamp}, {self.value!r}{status})"
    
    def __lt__(self, other):
        """Enable sorting and bisect operations."""
        if isinstance(other, VersionedValue):
            return self.timestamp < other.timestamp
        return self.timestamp < other
    
    def __eq__(self, other):
        if isinstance(other, VersionedValue):
            return self.timestamp == other.timestamp
        return self.timestamp == other

class TemporalKeyValueStore:
    """Key-value store with time-travel queries."""
    
    def __init__(self, precision=TimestampPrecision.SECOND):
        self.store = {}
        self.precision = precision
    
    def _normalize_timestamp(self, timestamp=None):
        """Round timestamp to configured precision."""
        if timestamp is None:
            timestamp = datetime.now()
        
        if self.precision == TimestampPrecision.MINUTE:
            timestamp = timestamp.replace(second=0, microsecond=0)
        else:  # SECOND
            timestamp = timestamp.replace(microsecond=0)
        
        return timestamp
    
    def put(self, key, value, timestamp=None):
        """Insert or update a value at timestamp."""
        timestamp = self._normalize_timestamp(timestamp)
        
        if key not in self.store:
            self.store[key] = [VersionedValue(timestamp, value)]
            return timestamp
        
        versions = self.store[key]
        index = bisect.bisect_right(versions, timestamp, key=lambda v: v.timestamp) - 1
        
        # If most recent version has same timestamp, update it
        if index >= 0 and versions[index].timestamp == timestamp:
            versions[index] = VersionedValue(timestamp, value)
        else:
            # Otherwise insert new version
            bisect.insort(versions, VersionedValue(timestamp, value), 
                         key=lambda v: v.timestamp)
        
        return timestamp
    
    def get(self, key):
        """Get current value."""
        if key not in self.store:
            logging.debug(f"Key '{key}' not found")
            return None
        
        versions = self.store[key]
        for version in reversed(versions):
            if not version.is_deleted:
                return version.value
        
        return None  # All versions deleted
    
    def get_at_time(self, key, timestamp):
        """Get value at specific point in time."""
        if key not in self.store:
            logging.debug(f"Key '{key}' not found")
            return None
        
        if timestamp is None:
            return self.get(key)
        
        timestamp = self._normalize_timestamp(timestamp)
        versions = self.store[key]
        
        # Find last version before or at this timestamp
        index = bisect.bisect_right(versions, timestamp, key=lambda v: v.timestamp) - 1
        
        if index < 0:
            return None  # Query time before first version
        
        version = versions[index]
        return None if version.is_deleted else version.value
    
    def delete(self, key, timestamp=None):
        """Soft delete: mark as deleted at timestamp."""
        if key not in self.store:
            logging.debug(f"Key '{key}' not found")
            return False
        
        timestamp = self._normalize_timestamp(timestamp)
        versions = self.store[key]
        
        # Insert deletion marker after last version at this time
        bisect.insort(versions, VersionedValue(timestamp, None, is_deleted=True),
                     key=lambda v: v.timestamp)
        return True
    
    def hard_delete(self, key):
        """Permanently remove all history (GDPR compliance)."""
        if key in self.store:
            del self.store[key]
            return True
        return False
    
    def get_history(self, key):
        """Return all versions for a key."""
        if key not in self.store:
            return []
        return self.store[key][:]  # Return copy
    
    def get_active_keys(self):
        """Return keys that haven't been deleted."""
        active = []
        for key, versions in self.store.items():
            for version in reversed(versions):
                if not version.is_deleted:
                    active.append(key)
                    break
        return active
```

---

## Testing Strategy

Test these scenarios:

1. **Basic Operations**
   - Put single value, get it back
   - Update same key multiple times
   - Get non-existent key → None

2. **Time-Travel Queries**
   - Query before first version → None
   - Query at exact timestamp → correct value
   - Query between two versions → older value
   - Query after all versions → current value

3. **Soft Delete**
   - Delete marks as deleted
   - Query before delete → returns value
   - Query after delete → returns None
   - History is preserved

4. **Timestamp Precision**
   - SECOND precision maintains microsecond differences as same
   - MINUTE precision groups puts within same minute
   - Round-trip: store and query uses same normalized time

5. **Edge Cases**
   - Empty store
   - Single version then query
   - Multiple deletes and undoes
   - Concurrent timestamps (bisect_right correctness)

---

## Summary of Recommendations

| Aspect | Recommendation | Rationale |
|--------|---|---|
| **Data Structure** | Use `VersionedValue` class | Clear semantics, extensible, debuggable |
| **Timestamp Storage** | Keep as `datetime` objects | Avoid string conversion bugs, enable rounding |
| **Precision** | Configurable (default SECOND) | Balances granularity with storage/performance |
| **Deletion** | Soft delete by default | Audit trail, time-travel works, GDPR-ready |
| **Binary Search** | Use `bisect_right() - 1` | Correct for "value at or before" queries |
| **Index Updates** | Use `bisect.insort()` | Maintains sorted order, cleaner than manual insert |

