"""

```

---

**Your tasks**

1. Fetch all listings across all pages
2. Filter out any invalid records (missing `id`, missing/empty `title`)
3. Normalize the data — trim whitespace from titles, lowercase `condition`, parse `price` as a float (skip the record if price can't be parsed)
4. Return only **active** listings
5. Print a summary report at the end:
```
Total listings fetched: X
Valid active listings: X
Average price: $X.XX
Conditions breakdown: {'good': X, 'fair': X, 'poor': X}
```

---

**Expected output** based on the mock data above:
```
Total listings fetched: 6
Valid active listings: 3
Average price: $91.67
Conditions breakdown: {'good': 2, 'poor': 1}
"""

import pandas as pd
import statistics
def mock_api(page: int) -> dict:
    data = {
        1: {"items": [
            {"id": "a1", "title": "  Lululemon Jacket ", "price": "120.00", "status": "active", "condition": "good"},
            {"id": "a2", "title": "North Face Vest", "price": "bad_price", "status": "active", "condition": "Fair"},
            {"id": "a3", "title": "New Balance Shoes", "price": "85.50", "status": "sold", "condition": "good"},
        ], "total_pages": 2},
        2: {"items": [
            {"id": "a4", "title": "", "price": "60.00", "status": "active", "condition": "poor"},
            {"id": "a5", "title": "Patagonia Fleece", "price": "95.00", "status": "active", "condition": "GOOD"},
            {"id": None, "title": "Ghost Item", "price": "10.00", "status": "active", "condition": "good"},
        ], "total_pages": 2},
    }
    return data.get(page, {"items": [], "total_pages": 2})

class ItemRetrieval:

    def __init__(self):
        self.pages = [1,2]

    def get_all_listings(self):
        data = {}
        count = 0
        if not self.pages: return None
        for page in self.pages:
            data[page] = mock_api(page)
            count += len(data[page]["items"])
        cleaned = self.filter_invalid_recs(data)

        avg_price = statistics.mean(float(item['price']) for item in cleaned)
        print(f"Total listings fetched: {count}")
        print(f"Valid active listings: {len(cleaned)}")
        print(f"Average price: {avg_price}")

    def filter_invalid_recs(self, data):
        if not data: return None
        clean_data = []
        for key in data.keys():
            items = data[key]["items"]
            if not items:
                raise ValueError("Invalid data passed in")
            for item in items:
                id = item["id"]
                title = item["title"]
                try:
                    s = item["price"]
                    price = float(s)
                except ValueError:
                    continue
                status = item["status"]
                if status != "active":
                    continue
                if not id or not title:
                    continue
                clean_data.append(item)
        return clean_data

i = ItemRetrieval()
i.get_all_listings()




