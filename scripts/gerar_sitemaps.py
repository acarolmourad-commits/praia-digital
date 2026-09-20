#!/usr/bin/env python3
"""Regenera sitemap.xml (paginas publicas) e sitemap-apps.xml (apps/).
Conservador: exclui secoes internas (dashboards, docs, outreach, partials, assets, api)."""
import os, urllib.parse, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://praia.digital/'
EXCLUDE_DIRS = {'backup','backups','docs','assets','partials','api','.git','.audit',
                '.github','.hermes-tmp-idempotency','node_modules','outreach','dashboards',
                'academy/uploads','backend','automation'}
EXCLUDE_FILES = {'404.html'}
EXCLUDE_PREFIX = ('obrigado-',)
TODAY = datetime.date.today().isoformat()

def excluded(rel):
    parts = rel.split('/')
    for i in range(len(parts)-1):
        if '/'.join(parts[:i+1]) in EXCLUDE_DIRS or parts[i] in EXCLUDE_DIRS:
            return True
    b = parts[-1]
    if b in EXCLUDE_FILES or b.startswith(EXCLUDE_PREFIX): return True
    return False

def priority(rel):
    if '/' not in rel: return '1.0' if rel == 'index.html' else '0.9'
    top = rel.split('/')[0]
    return {'blog':'0.8','bairros':'0.8','cidades':'0.8','imoveis':'0.9','apps':'0.7',
            'education':'0.7','academy':'0.7','ferramentas':'0.7','servicos':'0.8'}.get(top,'0.6')

pages, apps = [], []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if not d.startswith('.') and d != 'node_modules']
    for f in fn:
        if not f.endswith('.html'): continue
        rel = os.path.relpath(os.path.join(dp,f), ROOT).replace(os.sep,'/')
        if excluded(rel): continue
        (apps if rel.startswith('apps/') else pages).append(rel)

def write(path, urls):
    with open(path,'w',encoding='utf-8') as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fh.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in sorted(urls):
            loc = urllib.parse.quote(BASE+u, safe=':/')
            fh.write('<url><loc>%s</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>%s</priority></url>\n'
                     % (loc, TODAY, priority(u)))
        fh.write('</urlset>\n')

write(os.path.join(ROOT,'sitemap.xml'), pages)
write(os.path.join(ROOT,'sitemap-apps.xml'), apps)
print('sitemap.xml:', len(pages), 'URLs | sitemap-apps.xml:', len(apps), 'URLs')
