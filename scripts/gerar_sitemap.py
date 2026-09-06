#!/usr/bin/env python3
"""
Gera sitemap.xml com todas as páginas HTML do projeto.
"""

import re
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parent.parent
SITEMAP = BASE / "sitemap.xml"

# Padrões de exclusão
EXCLUDE_PATTERNS = [
    r'^aluno/',
    r'^assets/',
    r'^education/aluno/',
    r'^academy/',
    r'^backup(/|$)',
    r'/backup/',
    r'^\.',                     # arquivos/dirs ocultos
    r'(^|/)(__pycache__|node_modules|dist|build|tmp)(/|$)',
]

INDEXABLE_EXTENSIONS = {'.html', '.htm'}


def should_exclude(path: str) -> bool:
    # only consider indexable extensions
    if not any(path.lower().endswith(ext) for ext in INDEXABLE_EXTENSIONS):
        return True
    # skip drafts/templates/internal pages
    if any(token in path.lower() for token in ['/backup/', 'backup', 'draft', 'template', 'internal', 'temp-', '404.html']):
        return True
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, path, re.IGNORECASE):
            return True
    return False


def find_html_files(root: Path):
    paths = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(BASE)
        path_str = rel.as_posix()
        if should_exclude(path_str):
            continue
        if not any(path_str.lower().endswith(ext) for ext in INDEXABLE_EXTENSIONS):
            continue
        paths.append(path_str)
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
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"


def main():
    html_files = find_html_files(BASE)
    xml = build_sitemap(html_files)
    SITEMAP.write_text(xml, encoding="utf-8")
    print(f"sitemap.xml gerado com {len(html_files)} URLs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
