#!/usr/bin/env python3
"""Praia Digital 2026-10-24: corrige links internos quebrados verificados (issue #34, lote 1).

Idempotente. So reescreve um href/src quando o destino corrigido EXISTE
de fato no repositorio (arquivo, ou diretorio com index.html). Nunca
inventa destino. Regras:
- resolucao relativa a pagina falha, mas a interpretacao a partir da
  raiz existe -> usa o caminho relativo correto a partir da pagina;
- bairros/<cidade>-<bairro>.html -> bairros/<cidade>/<bairro>.html
  quando esse arquivo existe (split unico verificado);
- caminho cuja forma sem .html e um diretorio com index.html ->
  forma de diretorio com barra final;
- variantes de sufixo do site_fixer: sem .html -> .html existente,
  ou diretorio com index.html.
Pula externos, ancoras, mailto/tel/javascript/data, placeholders
${...}/{{...}}, URLs com %, destinos sem arquivo existente.
Nao altera anos, textos nem qualquer conteudo editorial.
"""
import pathlib
import posixpath
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LINK_RE = re.compile(r'((?:href|src)\s*=\s*["\'])([^"\']+)(["\'])', re.I)
SKIP_PREFIX = ('http://', 'https://', '//', 'mailto:', 'tel:', '#', 'javascript:', 'data:')
SKIP_DIRS = {'.git', 'node_modules', 'social'}


def is_file(rel):
    return (ROOT / rel).is_file()


def is_dir_index(rel):
    return (ROOT / rel / 'index.html').is_file()


def verified(rel):
    rel = posixpath.normpath(rel)
    if rel in ('.', '..') or rel.startswith('../') or rel.startswith('/'):
        return None
    if is_file(rel):
        return ('file', rel)
    if is_dir_index(rel):
        return ('dir', rel)
    return None


def candidates(page_dir, raw):
    found = {}

    def add(c):
        if c:
            found[c[1] + '|' + c[0]] = c

    stripped = raw
    while stripped.startswith('../'):
        stripped = stripped[3:]
    root_cand = posixpath.normpath(stripped.lstrip('/'))
    page_cand = posixpath.normpath(posixpath.join(page_dir, raw)) if page_dir else root_cand
    for base in (root_cand, page_cand):
        add(verified(base))
        add(verified(base + '.html'))
        if base.endswith('.html'):
            add(verified(base[:-5]))
    m = re.match(r'^bairros/([^/]+)\.html$', root_cand)
    if m:
        stem = m.group(1)
        parts = stem.split('-')
        splits = []
        for i in range(1, len(parts)):
            cand = 'bairros/' + '-'.join(parts[:i]) + '/' + '-'.join(parts[i:]) + '.html'
            v = verified(cand)
            if v:
                splits.append(v)
        if len(splits) == 1:
            add(splits[0])
    return list(found.values())


def fix_url(url, page_dir):
    if not url or url.startswith(SKIP_PREFIX):
        return None
    if '${' in url or '{{' in url or '%' in url:
        return None
    cut = len(url)
    for ch in ('#', '?'):
        i = url.find(ch)
        if i != -1:
            cut = min(cut, i)
    p, suffix = url[:cut], url[cut:]
    if not p:
        return None
    absolute = p.startswith('/')
    raw = p.lstrip('/') if absolute else p
    current = posixpath.normpath(raw) if (absolute or not page_dir) else posixpath.normpath(posixpath.join(page_dir, raw))
    if verified(current):
        return None
    cands = candidates(page_dir, raw)
    if len(cands) != 1:
        return False if not cands else None
    kind, target = cands[0]
    if kind == 'dir':
        out = ('/' + target + '/') if absolute else (posixpath.relpath(target, page_dir or '.') + '/')
    else:
        out = ('/' + target) if absolute else posixpath.relpath(target, page_dir or '.')
    new = out + suffix
    return new if new != url else None


def main():
    total = 0
    changed_files = 0
    skipped = 0
    html_files = [f for f in ROOT.rglob('*.html') if not (set(f.relative_to(ROOT).parts) & SKIP_DIRS)]
    for f in sorted(html_files):
        rel = f.relative_to(ROOT).as_posix()
        page_dir = posixpath.dirname(rel)
        text = f.read_text(encoding='utf-8', errors='surrogateescape')
        original = text
        count = [0]

        def repl(m):
            new = fix_url(m.group(2), page_dir)
            if new is False:
                return m.group(0)
            if new:
                count[0] += 1
                return m.group(1) + new + m.group(3)
            return m.group(0)

        text = LINK_RE.sub(repl, text)
        if text != original:
            f.write_text(text, encoding='utf-8', errors='surrogateescape')
            changed_files += 1
            total += count[0]
            print(f'{rel}: {count[0]} substituicao(oes)')
    print(f'TOTAL: {total} link(s) corrigido(s) em {changed_files} arquivo(s)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
