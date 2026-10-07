#!/usr/bin/env python3
"""Apply the homepage header to public HTML in the Pages artifact, byte-preserving other content."""
import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path

EXCLUDED = {'.git', '.github', '.audit', '.hermes-tmp-idempotency', 'backup', 'backups',
            'admin', 'api', 'backend', 'dashboard', 'dashboards', 'partials', 'templates',
            'tests', 'node_modules', 'uploads', 'csv-lotes-email'}
ASSETS = ('<link rel="stylesheet" href="/assets/css/pd-navigation.css?v=3">\n'
          '<script defer src="/js/pd-navigation.js?v=3"></script>\n')

IA_HEADINGS = {
    'ia/ia-mercado.html': 'IA para Análise de Mercado',
    'ia/ia-captacao.html': 'IA para Captação',
    'ia/ia-investidores.html': 'IA para Investidores',
    'ia/ia-marketing.html': 'IA para Marketing',
    'ia/ia-gestao.html': 'IA para Gestão',
}

def repair_heading(path, text):
    """Restore only known empty IA headings, using existing page titles."""
    title = IA_HEADINGS.get(path)
    if title is None:
        return text
    return re.sub(r'(<h1\b[^>]*>)\s*(?:&gt;|>)?\s*(</h1>)',
                  lambda m: m.group(1) + title + m.group(2),
                  text, count=1, flags=re.I)

class Layout(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text = text
        self.lines = [0]
        for match in re.finditer('\n', text):
            self.lines.append(match.end())
        self.stack = []
        self.ranges = []
        self.candidate = None
        self.body_end = None
        self.head_close = None
        self.redirect = False

    def pos(self):
        row, col = self.getpos()
        return self.lines[row - 1] + col

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        start = self.pos()
        end = start + len(self.get_starttag_text())
        classes = set(attrs.get('class', '').split())
        if tag == 'body':
            self.body_end = end
        if tag == 'meta':
            if attrs.get('http-equiv', '').lower() == 'refresh':
                self.redirect = True
            if attrs.get('name') == 'pd-shared-nav':
                self.ranges.append((start, end))
        if tag == 'header' and self.candidate is None:
            top = bool(self.stack and self.stack[-1] == 'body')
            known = bool(classes & {'pd-header', 'pd-nav', 'pd-site-header'})
            if top or known:
                self.candidate = [start, 'header', known or 'pd' in classes]
        elif tag == 'nav' and self.candidate is None and self.stack and self.stack[-1] == 'body' and 'pd-nav' in classes:
            self.candidate = [start, 'nav', True]
        if self.candidate and (tag == 'nav' or classes & {'logo', 'pd-logo', 'pd-site-logo'}):
            self.candidate[2] = True
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag == 'head':
            self.head_close = self.pos()
        if self.candidate and tag == self.candidate[1]:
            if self.candidate[2]:
                end = self.text.find('>', self.pos()) + 1
                self.ranges.append((self.candidate[0], end))
            self.candidate = None
        if tag in self.stack:
            self.stack = self.stack[:len(self.stack) - 1 - self.stack[::-1].index(tag)]

def preserve_header_intro(fragment):
    """Keep editorial headings, descriptions, forms and scripts from mixed legacy headers."""
    elements = [m.group(0) for m in re.finditer(
        r'<(?P<tag>h[1-6]|p|form|section|article|figure|picture|script|style)\b[^>]*>.*?</(?P=tag)\s*>',
        fragment, flags=re.I | re.S)]
    if not elements:
        return ''
    return ('<div class="pd-preserved-intro" style="max-width:1120px;margin:0 auto;padding:20px">'
            + ''.join(elements) + '</div>')

def transform(text, header):
    parsed = Layout(text)
    parsed.feed(text)
    if parsed.redirect or parsed.body_end is None or parsed.head_close is None:
        return text, False
    for start, end in sorted(parsed.ranges, reverse=True):
        fragment = text[start:end]
        intro = preserve_header_intro(fragment) if re.match(r'<header\b', fragment, re.I) else ''
        text = text[:start] + intro + text[end:]
    # Remove only assets owned by this builder; leave all application scripts/styles intact.
    text = re.sub(r'<link\b[^>]*href[^>]*?/assets/css/pd-navigation\.css[^>]*>\s*', '', text, flags=re.I)
    text = re.sub(r'<script\b[^>]*src[^>]*?/js/pd-navigation\.js[^>]*>\s*</script>\s*', '', text, flags=re.I)
    text = re.sub(r'</head\s*>', lambda m: ASSETS + m.group(), text, count=1, flags=re.I)
    text = re.sub(r'(<body\b[^>]*>)\s*', lambda m: m.group(1) + '\n' + header.rstrip() + '\n', text, count=1, flags=re.I)
    return text, True

def build(root):
    header = (root / 'partials/header.html').read_text(encoding='utf-8')
    report = {'included': [], 'skipped': []}
    for path in sorted(root.rglob('*.html')):
        rel = path.relative_to(root)
        if any(part in EXCLUDED or part.startswith('.') for part in rel.parts[:-1]):
            report['skipped'].append(str(rel))
            continue
        text = path.read_text(encoding='utf-8', errors='surrogateescape')
        prepared = repair_heading(rel.as_posix(), text)
        updated, included = transform(prepared, header)
        if included:
            from collections import Counter
            headings = lambda html: Counter(re.findall(r'<h1\b[^>]*>.*?</h1\s*>', html, re.I | re.S))
            if headings(prepared) != headings(updated):
                raise ValueError(f'Navigation build would alter content headings: {rel}')
        if included:
            path.write_text(updated, encoding='utf-8', errors='surrogateescape')
        report['included' if included else 'skipped'].append(str(rel))
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = build(args.root)
    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Navigation applied: {len(report['included'])}; skipped: {len(report['skipped'])}")
