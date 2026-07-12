
from pathlib import Path
from datetime import date

root = Path("C:/Users/Carolina/praia-digital")
base_url = "https://acarolmourad-commits.github.io/praia-digital/"

# Diretórios a excluir do sitemap
exclude_dirs = {".git", "node_modules", "backups", "scripts", "docs"}

html_files = []
for path in root.rglob("*.html"):
    rel_parts = path.relative_to(root).parts
    if any(part in exclude_dirs for part in rel_parts):
        continue
    if path.name.startswith("."):
        continue
    html_files.append(path.relative_to(root))

html_files.sort()

today = date.today().isoformat()
entries = []
for rel in html_files:
    loc = f"{base_url}{rel.as_posix()}"
    entries.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n  </url>")

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += "\n".join(entries)
sitemap += "\n</urlset>"

out_path = root / "sitemap.xml"
out_path.write_text(sitemap, encoding="utf-8")
print(f"Sitemap SEO-friendly atualizado com {len(entries)} URLs em {out_path}")
print("Inclui: index.html, blog/, imoveis/, marketing/, assets/ferramentas/, landing pages públicas")
print("Exclui: scripts/, docs/, backups/ e arquivos operacionais internos")
