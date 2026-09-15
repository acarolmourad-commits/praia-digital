#!/usr/bin/env python3
"""Auto-fix systematic broken internal links in static HTML pages.

Fixes two classes of errors:
1. Doubled path segments (e.g. blog/blog/post.html -> blog/post.html,
   docs/sales/docs/sales/x.html -> docs/sales/x.html)
2. Links to files that moved (resolved by unique basename match, or
   by progressively stripping leading path segments).

Only rewrites a link when the resolved target exists in the repo.
Skips internal/asset-only dirs: backup, backups, outreach, docs, .audit.
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

    def resolve(tgt, base):
        parts = tgt.split('/')
        # strip leading segments until something resolves
        for i in range(1, len(parts)):
            cand = '/'.join(parts[i:])
            if cand in allfiles:
                return cand
        # collapse doubled consecutive segments
        p2 = []
        for i, p in enumerate(parts):
            if i > 0 and p == parts[i - 1]:
                continue
            p2.append(p)
        cand = '/'.join(p2)
        if cand in allfiles:
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
            if tgt in allfiles or (tgt.rstrip('/') + '/index.html') in allfiles:
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
