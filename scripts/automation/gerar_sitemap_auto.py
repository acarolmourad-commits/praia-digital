import os, re
from pathlib import Path
from datetime import date

root = Path("C:/Users/Carolina/praia-digital")
exclude_dirs = {"node_modules", ".git", "outreach", "docs", "scripts", "assets", "imoveis", "blog"}
base_url = "https://acarolmourad-commits.github.io/praia-digital/"

html_files = []
for path in root.rglob("*.html"):
    rel = path.relative_to(root)
    if any(part in exclude_dirs for part in rel.parts):
        continue
    html_files.append(rel)

html_files.sort()

today = date.today().isoformat()
entries = []
for rel in html_files:
    loc = f"{base_url}{rel.as_posix()}"
    entries.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n  </url>")

sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += "\n".join(entries)
sitemap += "\n</urlset>"

out_path = root / "sitemap.xml"
out_path.write_text(sitemap, encoding="utf-8")
print(f"Sitemap atualizado com {len(entries)} URLs em {out_path}")
