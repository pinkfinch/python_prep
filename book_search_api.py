# You're building a feature for Archive's internal tools team that lets staff search for books about sustainable fashion and resale. Use the Open Library search API to power it.
# The API:
# GET https://openlibrary.org/search.json?q=<query>&page=<page>
# No API key needed. Returns JSON with a docs array and a numFound field.
#
# Your tasks
#
# Write a function that accepts a search query and a max_results parameter (default 10)
# Fetch pages until you have at least max_results items or run out of results
# For each result extract: title, author_name (first author only, if available), first_publish_year
# Skip any record missing both title and author_name
# Print a report:
#
# Search: "sustainable fashion"
# Results found: 10
#
# 1. Overdressed (Elizabeth Cline, 2012)
# 2. Fashionopolis (Dana Thomas, 2019)


import requests
import logging
class BookSearch:

    def __init__(self):
        self.log = logging.getLogger("book_search")

    def get_resp(self, query, max_results=10):
        if not query: return None
        data = []
        count = 0

        response = requests.get("https://openlibrary.org/search.json",
                                params = {
                                    "q":query,
                                    "page":1,
                                    "limit":max_results
                                })
        if response.status_code != 200:
            self.log.error(f"error response received: {response.status_code} with error: {response.reason}")
            return None
        resp = response.json()
        data.extend(resp["docs"])
        count = resp["numFound"]

        if not data: return None
        data = data[:max_results]
        print (f"Search: {query}")
        print (f"Results found: {count}")
        for idx, item in enumerate(data):
            title = item.get("title")
            author = item.get("author_name", [])
            if not title and not author:
                continue
            title = "Not specified" if not title else title
            author = "Not specified" if not author else author[0]
            publish_year = "N/A" if "first_publish_year" not in item else item["first_publish_year"]
            print(f'{idx+1}. {title} ({author}, {publish_year})')




b = BookSearch()
b.get_resp("sustainable fashion", 10)