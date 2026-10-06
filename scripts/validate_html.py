#!/usr/bin/env python3
"""Validador de HTML do blog (praia.digital).
Falha o CI se algum artigo de blog/*.html tiver:
- <h1> ausente, vazio ou quebrado (ex.: <h1>></h1>)
- mais de 1 <h1>
- <title> ausente/vazio ou padrao quebrado (<title>></title>)
Uso: python scripts/validate_html.py [dir]  (padrao: blog/)
Exit 1 com lista de problemas; exit 0 se tudo ok."""
import glob, html, os, re, sys

DIR = sys.argv[1] if len(sys.argv) > 1 else 'blog'
H1_RE = re.compile(r'<h1[^>]*>(.*?)</h1>', re.S | re.I)
TITLE_RE = re.compile(r'<title>(.*?)</title>', re.S | re.I)

problems = []
files = sorted(glob.glob(os.path.join(DIR, '*.html')))
for f in files:
    t = open(f, encoding='utf-8', errors='ignore').read()
    h1s = H1_RE.findall(t)
    if not h1s:
        problems.append(f'{f}: sem <h1>')
    elif len(h1s) > 1:
        problems.append(f'{f}: {len(h1s)} tags <h1> (esperado 1)')
    else:
        txt = html.unescape(re.sub(r'<[^>]+>', '', h1s[0])).strip()
        if not txt or txt == '>' or len(txt) < 5:
            problems.append(f'{f}: <h1> vazio/quebrado (conteudo: {txt!r})')
    m = TITLE_RE.search(t)
    if not m:
        problems.append(f'{f}: sem <title>')
    else:
        tt = html.unescape(m.group(1)).strip()
        if not tt or tt == '>':
            problems.append(f'{f}: <title> vazio/quebrado')

print(f'{len(files)} arquivos verificados em {DIR}/')
if problems:
    print(f'\n{len(problems)} problema(s):')
    for p in problems[:200]:
        print(' -', p)
    sys.exit(1)
print('OK: todos os artigos tem <h1> e <title> validos.')
