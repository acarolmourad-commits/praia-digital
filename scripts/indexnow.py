#!/usr/bin/env python3
"""IndexNow submission script for praia.digital sitemap."""
import json
import urllib.request
import urllib.parse
from pathlib import Path

API_KEY = "YOUR_INDEXNOW_API_KEY"
INDEXNOW_URL = "https://www.bing.com/indexnow"

sitemap = Path("sitemap.xml").read_text(encoding="utf-8")
urls = []
for line in sitemap.splitlines():
    if "<loc>" in line:
        urls.append(line.strip().replace("<loc>", "").replace("</loc>", ""))

payload = {
    "host": "praia.digital",
    "key": API_KEY,
    "urlList": urls,
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    INDEXNOW_URL,
    data=data,
    headers={"Content-Type": "application/json; charset=utf-8"},
    method="POST",
)

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        print("IndexNow response:", resp.status, resp.read().decode("utf-8", errors="ignore"))
except Exception as e:
    print("IndexNow error:", e)
