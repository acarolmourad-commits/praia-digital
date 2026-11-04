#!/usr/bin/env python3
"""Apply the owner's exact listing retirement scope before publication.

Uses only the standard library. HTML edits preserve bytes outside the affected
cards/schema blocks, and do not classify properties by city or numerical ID.
"""
import argparse
import csv
import io
import json
import os
import re
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'data/retired-listings.json'


def retired_slugs():
    return set(json.loads(MANIFEST.read_text(encoding='utf-8'))['slugs'])


def retired_url(value, slugs):
    if not isinstance(value, str):
        return False
    parts = urlsplit(unescape(value))
    if parts.netloc and parts.netloc not in {'praia.digital', 'www.praia.digital', 'acarolmourad.github.io', 'acarolmourad-commits.github.io'}:
        return False
    name = unquote(parts.path).rsplit('/', 1)[-1]
    if name == 'santos-apartamento-vista-mar.html':
        return True
    return name.endswith('.html') and name[:-5] in slugs


def retired_page(path, slugs):
    return ('imoveis' in path.parts or 'leads' in path.parts) and retired_url(path.as_posix(), slugs)


def notice(path):
    canonical = 'https://praia.digital/' + path.as_posix()
    return '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, follow">
  <meta name="pd-retired-listing" content="true">
  <title>Anúncio retirado | Praia Digital</title>
  <meta name="description" content="Este anúncio foi retirado. Consulte o catálogo atual da Praia Digital.">
  <link rel="canonical" href="''' + escape(canonical, quote=True) + '''">
  <style>
    *{box-sizing:border-box}body{margin:0;background:#f4f8fa;color:#153747;font:18px/1.6 system-ui,sans-serif}
    header,main{max-width:760px;margin:auto;padding:32px 24px}header a{color:#086b82;font-weight:700;text-decoration:none}
    main{margin:8vh auto;background:white;border:1px solid #dce7eb;border-radius:16px}
    h1{font-size:clamp(28px,5vw,40px);line-height:1.2}.button{display:inline-block;margin:16px 0;padding:12px 20px;border-radius:8px;background:#086b82;color:white;text-decoration:none}
    a:focus-visible{outline:3px solid #e5a100;outline-offset:4px}
  </style>
</head>
<body>
  <header><a href="/">Praia Digital</a></header>
  <main id="main">
    <h1>Anúncio retirado</h1>
    <p>Este anúncio foi retirado porque não corresponde a um imóvel cadastrado e confirmado para negociação.</p>
    <p>Consulte os imóveis disponíveis no catálogo atual.</p>
    <a class="button" href="/imoveis.html">Ver catálogo atual</a>
  </main>
</body>
</html>
'''


class Nodes(HTMLParser):
    VOID = set('area base br col embed hr img input link meta param source track wbr'.split())

    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text = text
        self.offsets = [0]
        for match in re.finditer('\n', text):
            self.offsets.append(match.end())
        self.nodes = []
        self.stack = []
        self.feed(text)
        self.close()

    def source_offset(self):
        line, column = self.getpos()
        return self.offsets[line - 1] + column

    def handle_starttag(self, tag, attrs):
        start = self.source_offset()
        node = {'tag': tag, 'attrs': dict(attrs), 'start': start,
                'end': start + len(self.get_starttag_text()),
                'parent': self.stack[-1] if self.stack else None}
        self.nodes.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.stack and self.stack[-1]['tag'] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index]['tag'] == tag:
                self.stack[index]['end'] = self.text.find('>', self.source_offset()) + 1
                del self.stack[index:]
                break


def clean_schema(value, slugs):
    if isinstance(value, list):
        return [v for item in value if (v := clean_schema(item, slugs)) is not None]
    if not isinstance(value, dict):
        return value
    if any(retired_url(value.get(k), slugs) for k in ['url', '@id', 'item']):
        return None
    result = {key: clean_schema(item, slugs) for key, item in value.items()}
    if result.get('@type') == 'ItemList' and result != value:
        for index, item in enumerate(result.get('itemListElement', []), 1):
            if isinstance(item, dict):
                item['position'] = index
        if 'numberOfItems' in result:
            result['numberOfItems'] = len(result.get('itemListElement', []))
    return result


def clean_html(text, slugs):
    parsed = Nodes(text)
    edits = []
    anchors = [n for n in parsed.nodes if n['tag'] == 'a']
    for node in anchors:
        if not retired_url(node['attrs'].get('href'), slugs):
            continue
        card = node
        parent = node['parent']
        while parent and parent['tag'] not in {'section', 'main', 'body'}:
            classes = set((parent['attrs'].get('class') or '').split())
            if parent['tag'] == 'article' or classes & {'property-card', 'imovel-card', 'servico-card', 'card'}:
                # Never remove a container holding a different property offer.
                other_details = [a for a in anchors if parent['start'] <= a['start'] < parent['end']
                                 and re.search(r'(?:imoveis/|\.html(?:[?#]|$))', a['attrs'].get('href') or '')
                                 and not retired_url(a['attrs'].get('href'), slugs)]
                if not other_details:
                    card = parent
            parent = parent['parent']
        replacement = '' if card is not node or 'servico-card' in (node['attrs'].get('class') or '') else '<a href="/imoveis.html">Consultar catálogo atual</a>'
        edits.append((card['start'], card['end'], replacement))
    for node in parsed.nodes:
        if node['tag'] == 'script' and node['attrs'].get('type') == 'application/ld+json':
            block = text[node['start']:node['end']]
            match = re.search(r'>(.*?)</script\s*>', block, re.S | re.I)
            if not match:
                continue
            try:
                original = json.loads(match[1])
            except ValueError:
                continue
            updated = clean_schema(original, slugs)
            if updated != original:
                replacement = '' if updated is None else '<script type="application/ld+json">\n' + json.dumps(updated, ensure_ascii=False, indent=2) + '\n</script>'
                edits.append((node['start'], node['end'], replacement))
    # Keep outermost removals and apply from the end, preserving all other bytes.
    chosen = []
    for edit in sorted(set(edits), key=lambda e: (e[0], -e[1])):
        if not chosen or edit[0] >= chosen[-1][1]:
            chosen.append(edit)
    for start, end, replacement in reversed(chosen):
        text = text[:start] + replacement + text[end:]
    return text


def clean_js(text, slugs):
    def replace(match):
        records = json.loads(match[2])
        kept = [p for p in records if p.get('slug') not in slugs]
        return match[0] if kept == records else match[1] + json.dumps(kept, ensure_ascii=False, indent=4) + ';'
    return re.sub(r'(const properties\s*=\s*)(\[[\s\S]*?\]);', replace, text)


def clean_xml(text, slugs):
    def replace(match):
        urls = re.findall(r'<loc>(.*?)</loc>|<link[^>]+href=["\']([^"\']+)', match[0], re.S)
        return '' if any(retired_url(a or b, slugs) for a, b in urls) else match[0]
    return re.sub(r'<(url|entry)\b[^>]*>.*?</\1>', replace, text, flags=re.S)


def clean_csv(text, slugs):
    rows = list(csv.reader(io.StringIO(text)))
    if not rows or 'slug' not in rows[0]:
        return text
    header = rows[0]
    index = header.index('slug')
    kept = [rows[0]]
    for row in rows[1:]:
        if len(row) > index and row[index] in slugs:
            continue
        kept.append([clean_html(value, slugs) if '<a ' in value else value for value in row])
    if kept == rows:
        return text
    out = io.StringIO(newline='')
    csv.writer(out, lineterminator='\n').writerows(kept)
    return out.getvalue()


def enforce(root=ROOT, apply=False):
    root = Path(root)
    slugs = retired_slugs()
    needles = {value.encode('utf-8') for slug in slugs | {'santos-apartamento-vista-mar'}
               for value in (slug, quote(slug), json.dumps(slug, ensure_ascii=True)[1:-1])}
    changed = []
    candidates = []
    for directory, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__', '.venv'}]
        for name in files:
            if name.endswith(('.html', '.xml')) or name in {'main.js', 'properties.json', 'landings.csv'}:
                candidates.append(Path(directory) / name)
    for path in sorted(candidates):
        rel = path.relative_to(root)
        payload = path.read_bytes()
        if not retired_page(rel, slugs) and not any(needle in payload for needle in needles):
            continue
        text = payload.decode('utf-8')
        updated = text
        if path.suffix == '.html':
            updated = notice(rel) if retired_page(rel, slugs) else clean_html(text, slugs)
        elif path.suffix == '.js' and path.name == 'main.js':
            updated = clean_js(text, slugs)
        elif path.suffix == '.xml':
            updated = clean_xml(text, slugs)
        elif path.suffix == '.csv' and path.name == 'landings.csv':
            updated = clean_csv(text, slugs)
        elif path.name == 'properties.json':
            records = json.loads(text)
            kept = [p for p in records if p.get('slug') not in slugs]
            if records != kept:
                updated = json.dumps(kept, ensure_ascii=False, indent=2) + '\n'
        if updated != text:
            changed.append(rel.as_posix())
            if apply:
                path.write_text(updated, encoding='utf-8', newline='')
    return changed


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    changes = enforce(args.root, args.apply)
    print(json.dumps({'mode': 'apply' if args.apply else 'check', 'changed': changes}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if args.apply or not changes else 1)
