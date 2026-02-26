# import time
#

# ```

#
# **Your tasks**
#
# 1. Fetch all pages from **both** endpoints
# 2. Parse and normalize each item (strip whitespace, parse price as float, skip invalid records)
# 3. Merge into a single collection, tagging each item with its source (`active` or `sold`)
# 4. Detect any items appearing in both feeds (same `id`) and flag them as conflicts
# 5. Print a report:
# ```
# Total active listings: 5
# Total sold listings: 3
# Conflicts detected: 1
#   - p2: North Face Vest appears in both active and sold feeds

def get_active_listings(page: int) -> dict:
    data = {
        1: {"items": [
            {"id": "p1", "title": "Lululemon Jacket", "price": "120.00"},
            {"id": "p2", "title": "North Face Vest", "price": "85.00"},
            {"id": "p3", "title": "New Balance Shoes", "price": "60.00"},
        ], "total_pages": 2},
        2: {"items": [
            {"id": "p4", "title": "Patagonia Fleece", "price": "95.00"},
            {"id": "p5", "title": "Arc'teryx Jacket", "price": "200.00"},
        ], "total_pages": 2},
    }
    return data.get(page, {"items": [], "total_pages": 2})

def get_sold_listings(page: int) -> dict:
    data = {
        1: {"items": [
            {"id": "p6", "title": "Adidas Hoodie", "price": "45.00"},
            {"id": "p2", "title": "North Face Vest", "price": "85.00"},  # duplicate!
            {"id": "p7", "title": "Nike Joggers", "price": "55.00"},
        ], "total_pages": 1},
    }
    return data.get(page, {"items": [], "total_pages": 1})

class JacketListings:

    def __init__(self):
        pass

    def fetch_all_pages(self,api_func) -> list[dict]:
        results = []
        page = 1
        while True:
            resp = api_func(page)
            if not resp:
                break
            results.extend(resp.get("items", []))
            if page >= resp["total_pages"]:
                break
            page += 1
        return results

    def retrieve_active_listings(self):
        data = []
        active_listings = []
        data = self.fetch_all_pages(get_active_listings)
        for item in data:
            try:
                id = item["id"].strip()
                title = item["title"].strip()
                price = float(item["price"])
                active_listings.append(
                    {"id": id, "title": title, "price": price, "source": "active"},
                )
            except:
                print(f"Skipping invalid item: {item}")
                continue
        return active_listings

    def retrieve_sold_listings(self):
        data = []
        sold_listings = []
        data = self.fetch_all_pages(get_sold_listings)

        if not data: return None
        for item in data:
            try:
                id = item["id"].strip()
                title = item["title"].strip()
                price = float(item["price"])
                sold_listings.append(
                    {"id": id, "title": title, "price": price, "source": "sold"},
                )
            except:
                print(f"Skipping invalid item: {item}")
                continue
        return sold_listings

    def fetch_all_data(self):
        active_listings = self.retrieve_active_listings() or []
        sold_listings = self.retrieve_sold_listings() or []

        active_ids = {item["id"] for item in active_listings}
        sold_ids = {item["id"] for item in sold_listings}
        conflict_ids = active_ids & sold_ids

        all_listings = active_listings + sold_listings

        print(f"Total active listings: {len(active_listings)}")
        print(f"Total sold listings: {len(sold_listings)}")
        print(f"Conflicts detected: {len(conflict_ids)}")
        for item_id in conflict_ids:
            title = next(i["title"] for i in all_listings if i["id"] == item_id)
            print(f"  - {item_id}: {title} appears in both active and sold feeds")


j = JacketListings()
j.fetch_all_data()