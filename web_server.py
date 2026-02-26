from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import requests
import json


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if parsed.path == "/search":
            # your logic here
            pass
        elif parsed.path.startswith("/book/"):
            # your logic here
            pass
        else:
            self.send_error(404, "Not found")

    def send_json(self, status_code, data):
        # helper to send JSON responses
        pass


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8080), Handler)
    print("Server running on port 8080")
    server.serve_forever()