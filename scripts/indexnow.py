#!/usr/bin/env python3
"""IndexNow submission for praia.digital (Bing/Yandex/Naver/Seznam)."""
import json, os, urllib.request
from pathlib import Path

API_KEY = os.environ.get("INDEXNOW_API_KEY") or "cc1bbcd22d7bd74899c59b18e7675803"
INDEXNOW_URL = "https://api.indexnow.org/indexnow"
HOST = "praia.digital"

urls = []
for sm in ("sitemap.xml", "sitemap-apps.xml"):
    p = Path(sm)
    if not p.exists():
        continue
    for line in p.read_text(encoding="utf-8").splitlines():
        if "<loc>" in line:
            urls.append(line.strip().replace("<loc>", "").replace("</loc>", ""))

print("URLs a enviar:", len(urls))
if not urls:
    raise SystemExit("nenhuma URL encontrada")

# IndexNow aceita ate 10.000 URLs por requisicao
for i in range(0, len(urls), 10000):
    batch = urls[i:i+10000]
    payload = {"host": HOST, "key": API_KEY,
               "keyLocation": f"https://{HOST}/{API_KEY}.txt",
               "urlList": batch}
    req = urllib.request.Request(
        INDEXNOW_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            print(f"lote {i//10000+1}: HTTP {resp.status} ({len(batch)} URLs)")
    except urllib.error.HTTPError as e:
        print(f"lote {i//10000+1}: HTTP {e.code} {e.read().decode('utf-8', errors='ignore')[:200]}")
    except Exception as e:
        print("IndexNow error:", e)
