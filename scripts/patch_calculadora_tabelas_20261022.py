#!/usr/bin/env python3
# Patch unico (22/10/2026): calculadora ROI temporada - tabelas vazadas.
# Envolve as 7 tabelas estaticas em .table-scroll, adiciona CSS responsivo
# e aborta se o marcador ja existir (idempotente).
import re, subprocess, sys

PATH = 'ferramentas/calculadora-roi-temporada.html'
MARKER = 'FIX table leak 2026-10-22'
CSS = """
    /* FIX table leak 2026-10-22: tabelas contidas, rolaveis e legiveis */
    .card,.wrap{min-width:0;max-width:100%}
    .table-scroll{width:100%;max-width:100%;overflow-x:auto;overflow-y:hidden;-webkit-overflow-scrolling:touch;margin-top:12px;border:1px solid #e5e7eb;border-radius:10px;background:#fff}
    .table-scroll:focus{outline:2px solid #0e7c7b;outline-offset:2px}
    .table-scroll table{width:100%;min-width:580px;margin-top:0;border-collapse:collapse}
    .table-scroll.tight table{min-width:460px}
    .table-scroll th,.table-scroll td{vertical-align:top;overflow-wrap:break-word}
    @media (max-width:640px){
      .wrap{padding:20px 14px}
      .card{padding:14px}
      .table-scroll th,.table-scroll td{font-size:13px;padding:7px 8px;line-height:1.45}
      .bar-row{grid-template-columns:108px 1fr 82px;font-size:12px;gap:6px}
    }
"""

t = open(PATH, encoding='utf-8').read()
if MARKER in t:
    print('patch ja aplicado')
    sys.exit(0)
idx = t.find('</style>')
if idx == -1:
    print('ERRO: </style> nao encontrado')
    sys.exit(1)
t = t[:idx] + CSS + t[idx:]

parts = re.split(r'(<script\b.*?</script>)', t, flags=re.S | re.I)
wrapped = 0

def repl(m):
    tbl = m.group(0)
    first = re.search(r'<tr[^>]*>(.*?)</tr>', tbl, flags=re.S | re.I)
    cols = len(re.findall(r'<t[hd]\b', first.group(1), re.I)) if first else 0
    cls = 'table-scroll tight' if cols <= 3 else 'table-scroll'
    return '<div class="' + cls + '" tabindex="0" role="region" aria-label="Tabela com rolagem horizontal se necessario">' + tbl + '</div>'

for i, part in enumerate(parts):
    if part.lower().startswith('<script'):
        continue
    parts[i], n = re.subn(r'<table\b[^>]*>.*?</table>', repl, part, flags=re.S | re.I)
    wrapped += n

if wrapped != 7:
    print('ERRO: esperadas 7 tabelas estaticas, encontradas', wrapped)
    sys.exit(1)

open(PATH, 'w', encoding='utf-8').write(''.join(parts))
subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'], check=True)
subprocess.run(['git', 'config', 'user.email', 'github-actions[bot]@users.noreply.github.com'], check=True)
subprocess.run(['git', 'add', PATH], check=True)
subprocess.run(['git', 'commit', '-m', 'fix(calculadora): corrige vazamento das tabelas ROI temporada'], check=True)
subprocess.run(['git', 'push'], check=True)
print('PATCH APLICADO E PUSHADO - 7 tabelas envolvidas')
