#!/usr/bin/env python3
"""Remove todos os breadcrumbs do site (idempotente): nav visivel, CSS orfao e JSON-LD BreadcrumbList."""
import re, glob, json

script_re = re.compile(r'[ \t]*<script type="application/ld\+json">(.*?)</script>\s*\n?', re.S)
nav_re  = re.compile(r'[ \t]*<nav\b[^>]*aria-label="[Bb]readcrumb"[^>]*>.*?</nav>\s*\n?', re.S)
div_re  = re.compile(r'[ \t]*<div class="breadcrumbs?">.*?</div>\s*\n?', re.S)
css_re  = re.compile(r'\s*\.breadcrumbs?\s*\{[^}]*\}')
stats = {'jsonld':0,'jsonld_node':0,'nav':0,'div':0,'css':0,'files':0}

def process_block(m):
    b = m.group(1)
    if 'BreadcrumbList' not in b: return m.group(0)
    types = set(re.findall(r'"@type"\s*:\s*"([^"]+)"', b))
    if not (types - {'BreadcrumbList','ListItem'}):
        stats['jsonld'] += 1; return ''
    try:
        d = json.loads(b)
        def strip(x):
            if isinstance(x, dict):
                if x.get('@type') == 'BreadcrumbList': return None
                out = {}
                for k,v in x.items():
                    sv = strip(v)
                    if sv is not None: out[k] = sv
                return out
            if isinstance(x, list):
                return [e for e in (strip(i) for i in x) if e is not None]
            return x
        stats['jsonld_node'] += 1
        return m.group(0).replace(b, '\n' + json.dumps(strip(d), ensure_ascii=False, indent=2) + '\n')
    except Exception:
        return m.group(0)

for f in glob.glob('**/*.html', recursive=True):
    t = open(f, encoding='utf-8', errors='ignore').read(); o = t
    t = script_re.sub(process_block, t)
    t, n1 = nav_re.subn('', t); t, n2 = div_re.subn('', t); t, n3 = css_re.subn('', t)
    stats['nav'] += n1; stats['div'] += n2; stats['css'] += n3
    if t != o:
        open(f, 'w', encoding='utf-8').write(t); stats['files'] += 1
print(stats)
