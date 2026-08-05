#!/usr/bin/env python3
"""
Atualiza o sitemap.xml com páginas existentes do projeto.
Uso:
  python scripts/sync_sitemap.py
"""

import re
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parent.parent
SITEMAP = BASE / "sitemap.xml"


def find_html_files(root: Path):
    paths = []
    for p in root.rglob("*.html"):
        rel = p.relative_to(BASE)
        paths.append(rel.as_posix())
    return sorted(set(paths))


def build_sitemap(paths):
    today = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    urls = []
    for path in paths:
        loc = f"https://praia.digital/{path}"
        urls.append(
            f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>"""
        )
    return "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n" + "\n".join(urls) + "\n</urlset>\n"


def main():
    html_files = find_html_files(BASE)
    xml = build_sitemap(html_files)
    SITEMAP.write_text(xml, encoding="utf-8")
    print(f"sitemap.xml atualizado com {len(html_files)} URLs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
