
from pathlib import Path
from datetime import date
from urllib.parse import quote

root = Path("C:/Users/Carolina/praia-digital")
base_url = "https://acarolmourad-commits.github.io/praia-digital/"

include_dirs = {"", "blog", "imoveis", "marketing", "assets", "cases", "newsletter", "parcerias-litoral-paulista.html"}
allowed_exts = {".html"}

html_files = []
for path in root.rglob("*"):
    if not path.is_file():
        continue
    if path.suffix.lower() not in allowed_exts:
        continue
    if path.name.startswith("."):
        continue
    rel = path.relative_to(root)
    top = rel.parts[0] if rel.parts else ""
    if top == "docs":
        continue
    # inclui raiz + pastas permitidas
    if top not in include_dirs and rel.name != "index.html":
        continue
    html_files.append(rel)

html_files.sort()

today = date.today().isoformat()
entries = []
for rel in html_files:
    safe_loc = base_url + quote(str(rel).replace("\\", "/"), safe="/:-_.~")
    entries.append(
        "  <url>\n"
        f"    <loc>{safe_loc}</loc>\n"
        f"    <lastmod>{today}</lastmod>\n"
        "    <changefreq>weekly</changefreq>\n"
        "  </url>"
    )

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += "\n".join(entries)
sitemap += "\n</urlset>\n"

out_path = root / "sitemap.xml"
out_path.write_text(sitemap, encoding="utf-8")
print(f"Sitemap sanitizado atualizado com {len(entries)} URLs")
print("Verificando XML...")
import xml.etree.ElementTree as ET
ET.parse(out_path)
print("Sitemap XML válido")
