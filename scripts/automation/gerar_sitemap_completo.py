
from pathlib import Path
from datetime import date

root = Path("C:/Users/Carolina/praia-digital")
base_url = "https://acarolmourad-commits.github.io/praia-digital/"

# Pastas irrelevantes para sitemap
exclude_dirs = {".git", "node_modules", "backups"}

html_files = []
for path in root.rglob("*.html"):
    rel_parts = path.relative_to(root).parts
    if any(part in exclude_dirs for part in rel_parts):
        continue
    # Ignora arquivos sem nome significativo
    if path.name.startswith("."):
        continue
    html_files.append(path.relative_to(root))

html_files.sort()

today = date.today().isoformat()
entries = []
for rel in html_files:
    # Monta URL relativa estável
    rel_posix = rel.as_posix()
    loc = f"{base_url}{rel_posix}"
    entries.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n  </url>")

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += "\n".join(entries)
sitemap += "\n</urlset>"

out_path = root / "sitemap.xml"
out_path.write_text(sitemap, encoding="utf-8")
print(f"Sitemap completo atualizado com {len(entries)} URLs em {out_path}")
