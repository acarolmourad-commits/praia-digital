#!/usr/bin/env python3
"""Corrige <h1>></h1> quebrado nos artigos do blog usando o <title> da pagina."""
import glob, html, os, re, subprocess

fixed = []
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
for f in glob.glob('blog/*.html'):
    with open(f, encoding='utf-8', errors='ignore') as fh:
        t = fh.read()
    if '<h1>></h1>' not in t:
        continue
    m = re.search(r'<title>(.*?)</title>', t, re.S | re.I)
    if not m:
        continue
    title = html.unescape(m.group(1)).strip()
    t = t.replace('<h1>></h1>', '<h1>' + html.escape(title) + '</h1>', 1)
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
