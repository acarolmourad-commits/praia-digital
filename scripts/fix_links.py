#!/usr/bin/env python3
"""Auto-fix systematic broken internal links in static HTML pages. v2

Fix classes:
1. Doubled path segments (blog/blog/x.html -> blog/x.html)
2. Moved files (unique basename match / strip leading segments)
3. Missing page but directory with index.html exists
   (hub/automacao-imobiliaria.html -> hub/automacao-imobiliaria/index.html)
4. Missing page whose parent dir has index.html (page -> dir/index.html)

Only rewrites a link when the resolved target exists in the repo.
Skips internal/asset-only dirs: backup, backups, outreach, docs, .audit.
Empty href="" is left untouched (usually JS-filled placeholders).
"""
import os
import re
import json
from urllib.parse import urldefrag

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = ('backup', 'backups', 'outreach', 'docs', '.audit', '.git')
HREF = re.compile(r'href="([^"]+)"')

def main():
    allfiles = set()
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d != '.git']
        for f in fn:
            allfiles.add(os.path.relpath(os.path.join(dp, f), ROOT).replace('\\', '/'))
    htmlfiles = sorted(f for f in allfiles if f.endswith('.html'))
    byname = {}
    for f in allfiles:
        byname.setdefault(os.path.basename(f), []).append(f)

    def exists(t):
        return t in allfiles

    def resolve(tgt, base):
        parts = tgt.split('/')
        # 3a. page.html missing but page/index.html exists
        if tgt.endswith('.html'):
            cand = tgt[:-5].rstrip('/') + '/index.html'
            if exists(cand):
                return cand
        # 3b. directory index
        if exists(tgt.rstrip('/') + '/index.html'):
            return tgt.rstrip('/') + '/index.html'
        # strip leading segments until something resolves
        for i in range(1, len(parts)):
            cand = '/'.join(parts[i:])
            if exists(cand):
                return cand
        # collapse doubled consecutive segments
        p2 = []
        for i, p in enumerate(parts):
            if i > 0 and p == parts[i - 1]:
                continue
            p2.append(p)
        cand = '/'.join(p2)
        if exists(cand):
            return cand
        # unique basename anywhere, prefer same top-level dir, then root
        bn = os.path.basename(tgt)
        cands = byname.get(bn, [])
        if bn and len(cands) == 1:
            return cands[0]
        if cands:
            top = base.split('/')[0] if base else ''
            for c in cands:
                if c.split('/')[0] == top:
                    return c
            for c in cands:
                if '/' not in c:
                    return c
        # 4. parent directory index as last resort
        parent = os.path.dirname(tgt)
        while parent and parent != '.':
            cand = parent.rstrip('/') + '/index.html'
            if exists(cand):
                return cand
            parent = os.path.dirname(parent)
        return None

    fixed_files = 0
    fixed_links = 0
    for rel in htmlfiles:
        if rel.split('/')[0] in SKIP_DIRS:
            continue
        p = os.path.join(ROOT, rel)
        base = os.path.dirname(rel)
        html = open(p, encoding='utf-8', errors='ignore').read()
        n = 0
        for href in set(HREF.findall(html)):
            o = href.strip()
            if not o or o.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'data:')):
                continue
            if o.startswith(('http://', 'https://', '//')):
                continue
            path = urldefrag(o)[0].split('?')[0]
            if not path:
                continue
            tgt = path.lstrip('/') if path.startswith('/') else os.path.normpath(os.path.join(base, path)).replace('\\', '/')
            if exists(tgt) or exists(tgt.rstrip('/') + '/index.html'):
                continue
            f = resolve(tgt, base)
            if not f:
                continue
            newrel = ('/' + f) if path.startswith('/') else os.path.relpath(f, base).replace('\\', '/')
            suffix = o[len(urldefrag(o)[0]):]
            tag = 'href="%s"' % o
            if tag in html:
                html = html.replace(tag, 'href="%s"' % (newrel + suffix))
                n += 1
        if n:
            open(p, 'w', encoding='utf-8').write(html)
            fixed_files += 1
            fixed_links += n
    print(json.dumps({'fixed_files': fixed_files, 'fixed_links': fixed_links}))

if __name__ == '__main__':
    main()
