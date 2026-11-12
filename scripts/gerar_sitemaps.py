#!/usr/bin/env python3
"""Regenera sitemap.xml (paginas publicas) e sitemap-apps.xml (apps/).
Conservador: exclui secoes internas (dashboards, fixtures de teste, outreach, partials, assets, api)."""
import os, urllib.parse, datetime
import xml.etree.ElementTree as ET
from pathlib import Path

if __package__:
    from .validate_sitemap_targets import (indexing_exclusions, excluded_path, robots_rules, blocked_by_robots, IndexingDirectives, canonical_sitemap_path)
else:
    from validate_sitemap_targets import (indexing_exclusions, excluded_path, robots_rules, blocked_by_robots, IndexingDirectives, canonical_sitemap_path)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://praia.digital/'
TODAY = datetime.date.today().isoformat()


def excluded(rel):
    return excluded_path(rel)


def priority(rel):
    if '/' not in rel: return '1.0' if rel in ('', 'index.html') else '0.9'
    top = rel.split('/')[0]
    return {'blog':'0.8','bairros':'0.8','cidades':'0.8','imoveis':'0.9','apps':'0.7',
            'education':'0.7','academy':'0.7','ferramentas':'0.7','servicos':'0.8'}.get(top,'0.6')

def discover_pages(root):
    """Collect public pages without indexing explicit noindex/redirect pages."""
    pages, apps = [], []
    rules = robots_rules(Path(root))
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if not d.startswith('.') and d != 'node_modules']
        for f in fn:
            if not f.endswith('.html'):
                continue
            path = Path(dp) / f
            rel = os.path.relpath(path, root).replace(os.sep, '/')
            if excluded(rel) or blocked_by_robots("/" + rel, rules) or indexing_exclusions(path):
                continue
            rel = canonical_sitemap_path(path, Path(root))
            if rel is None:
                continue
            (apps if rel.startswith('apps/') else pages).append(rel)
    return pages, apps


def write(path, urls):
    # Reuse known dates. A checkout timestamp or generator run is not a content update.
    dates = {}
    if os.path.exists(path):
        try:
            for entry in ET.parse(path).findall('.//{*}url'):
                loc, lastmod = entry.find('{*}loc'), entry.find('{*}lastmod')
                if loc is not None and lastmod is not None:
                    dates[urllib.parse.unquote(loc.text or '')] = lastmod.text
        except ET.ParseError:
            pass
    with open(path,'w',encoding='utf-8') as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fh.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in sorted(set(urls)):
            loc = urllib.parse.quote(BASE+u, safe=':/')
            known_date = dates.get(urllib.parse.unquote(loc))
            date_tag = '<lastmod>%s</lastmod>' % known_date if known_date else ''
            fh.write('<url><loc>%s</loc>%s<changefreq>weekly</changefreq><priority>%s</priority></url>\n'
                     % (loc, date_tag, priority(u)))
        fh.write('</urlset>\n')

def main(root=None):
    root = ROOT if root is None else root
    pages, apps = discover_pages(root)
    write(os.path.join(root, 'sitemap.xml'), pages)
    write(os.path.join(root, 'sitemap-apps.xml'), apps)
    print('sitemap.xml:', len(pages), 'URLs | sitemap-apps.xml:', len(apps), 'URLs')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
