#!/usr/bin/env python3
"""Corrige h1 quebrado/ausente nos artigos do blog usando o <title> da pagina.
Casos cobertos:
1. <h1>></h1> (bug do commit 8e911f5c) -> substitui pelo title
2. Artigo sem <h1> -> insere <h1> logo apos o primeiro <article>
Remove o sufixo ' | Praia Digital' do title para o h1."""
import glob, html, os, re, subprocess

H1_RE = re.compile(r'<h1[^>]*>(.*?)</h1>', re.S | re.I)
TITLE_RE = re.compile(r'<title>(.*?)</title>', re.S | re.I)

fixed = []
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
for f in glob.glob('blog/*.html'):
    with open(f, encoding='utf-8', errors='ignore') as fh:
        t = fh.read()
    orig = t
    m = TITLE_RE.search(t)
    if not m:
        continue
    title = html.unescape(m.group(1)).strip()
    title = re.sub(r'\s*\|\s*Praia Digital\s*$', '', title).strip() or title
    h1s = H1_RE.findall(t)
    if '<h1>></h1>' in t:
        t = t.replace('<h1>></h1>', '<h1>' + html.escape(title) + '</h1>', 1)
    elif not h1s and '<article>' in t:
        t = t.replace('<article>', '<article>\n<h1>' + html.escape(title) + '</h1>', 1)
    if t != orig:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(t)
        fixed.append(f)
print(f'{len(fixed)} arquivos corrigidos')
if fixed:
    subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'], check=True)
    subprocess.run(['git', 'config', 'user.email', 'github-actions[bot]@users.noreply.github.com'], check=True)
    subprocess.run(['git', 'add'] + fixed, check=True)
    subprocess.run(['git', 'commit', '-m', f'fix(blog): restaura <h1> com o titulo da pagina em {len(fixed)} artigos [skip ci]'], check=True)
    subprocess.run(['git', 'push'], check=True)
