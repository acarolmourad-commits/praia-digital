#!/usr/bin/env python3
"""Corrige header mobile em imoveis.html e ferramentas/calculadora-roi-temporada.html (one-shot, 2026-09-28)."""
import re

# --- 1) calculadora: mover marcador pd-shared-nav para logo apos <body> e remover CSS legado de header
f = 'ferramentas/calculadora-roi-temporada.html'
t = open(f, encoding='utf-8').read()
# remove legacy header css rule
t = re.sub(r'\s*header nav a \{[^}]*\}', '', t)
# extract marker from inside .wrap and place right after <body>
m = re.search(r'\s*<meta name="pd-shared-nav">', t)
assert m, 'marker not found'
t = t.replace(m.group(0), '', 1)
t = re.sub(r'<body>', '<body>\n  <meta name="pd-shared-nav">', t, count=1)
open(f, 'w', encoding='utf-8').write(t)
assert 'header nav a' not in t and t.index('pd-shared-nav') < t.index('class="wrap"')
print('OK calculadora')

# --- 2) imoveis.html: stylesheet carrega direto (sem hack media=print)
f = 'imoveis.html'
t = open(f, encoding='utf-8').read()
old = '<link rel="stylesheet" href="https://praia.digital/css/style.css?v=3" media="print" onload="this.media=\'all\'">'
assert old in t, 'stylesheet link not found'
t = t.replace(old, '<link rel="stylesheet" href="https://praia.digital/css/style.css?v=4">')
open(f, 'w', encoding='utf-8').write(t)
print('OK imoveis')
