import os, re, json, html

STYLE = """
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:15px;background:#FFFFFF;color:#023047}
th{background:#0077B6;color:#FFFFFF;text-align:left;padding:10px}
td{border:1px solid #d0d7de;padding:9px;color:#023047;vertical-align:top}
tr:nth-child(even){background:#f6f8fa}
.bar-wrap{background:#e5e7eb;border-radius:6px;overflow:hidden;margin:4px 0 14px}
.bar{background:#0077B6;color:#FFFFFF;padding:6px 10px;font-size:13px;white-space:nowrap}
.bar.green{background:#2d9e5a}.bar.orange{background:#F97316}
"""

def esc(s): return html.escape(s.strip())

def parse_course(slug):
    base = f'education/cursos/{slug}/curso-completo'
    mods = {}
    if not os.path.isdir(base): return None
    for fn in sorted(os.listdir(base)):
        m = re.match(r'modulo-(\d+)\.md$', fn)
        if not m: continue
        t = open(os.path.join(base, fn), encoding='utf-8').read()
        aulas = re.findall(r'^## Aula [\d.]+ [\u2014-] (.+)$', t, flags=re.M)
        mods[int(m.group(1))] = [esc(a) for a in aulas]
    names = {}
    sfile = os.path.join(base, 'sumario.md')
    if os.path.isfile(sfile):
        s = open(sfile, encoding='utf-8').read()
        for m in re.finditer(r'M\u00f3dulo (\d+):\s*(.+)', s):
            names[int(m.group(1))] = esc(m.group(2))
    return mods, names

def build_table(mods, names):
    rows, bars = [], []
    total_aulas = sum(len(v) for v in mods.values()) or 1
    for n in sorted(mods):
        aulas = mods[n]
        nome = names.get(n, f'M\u00f3dulo {n}')
        lis = '<br>'.join(f'\u2022 {a}' for a in aulas) if aulas else '\u2014'
        rows.append(f'<tr><td>{n}</td><td><strong>{nome}</strong></td><td>{lis}</td><td>{len(aulas)}</td></tr>')
        pct = max(8, round(len(aulas)/total_aulas*100))
        color = 'bar' if n % 3 == 1 else ('bar green' if n % 3 == 2 else 'bar orange')
        bars.append(f'<p>{nome}</p><div class="bar-wrap"><div class="{color}" style="width:{pct}%">{len(aulas)} aulas</div></div>')
    table = ('<table><tr><th>#</th><th>M\u00f3dulo</th><th>Aulas</th><th>Total</th></tr>'
             + ''.join(rows) + '</table>')
    chart = '<p><strong>Distribui\u00e7\u00e3o de aulas por m\u00f3dulo:</strong></p>' + ''.join(bars)
    return table + chart

def meta_table(price):
    return (f'<table><tr><th>Investimento</th><th>Formato</th><th>Acesso</th><th>Certificado</th><th>Garantia</th></tr>'
            f'<tr><td>{price}</td><td>100% online</td><td>Imediato e vital\u00edcio</td><td>Autom\u00e1tico</td><td>7 dias</td></tr></table>')

report = {"cursos": 0, "formacoes": 0, "skipped": []}

for slug in sorted(os.listdir('education/cursos')):
    ipath = f'education/cursos/{slug}/index.html'
    if not os.path.isfile(ipath): continue
    parsed = parse_course(slug)
    if not parsed or not parsed[0]:
        report["skipped"].append(slug); continue
    mods, names = parsed
    t = open(ipath, encoding='utf-8').read()
    m = re.search(r'<h2>Conte\u00fado program\u00e1tico</h2>(.*?)(?=<div class="faq">|<h2>)', t, flags=re.S)
    if not m:
        report["skipped"].append(slug); continue
    price_m = re.search(r'<div class="price"[^>]*>([^<]+)</div>', t)
    price = esc(price_m.group(1)) if price_m else 'Consulte'
    newsec = build_table(mods, names) + '\n<h2>Informa\u00e7\u00f5es do curso</h2>\n' + meta_table(price)
    t = t[:m.start(1)] + '\n' + newsec + '\n' + t[m.end(1):]
    if '</style>' in t and 'th{background:#0077B6' not in t:
        t = t.replace('</style>', STYLE + '</style>', 1)
    open(ipath, 'w', encoding='utf-8').write(t)
    report["cursos"] += 1

for fn in sorted(os.listdir('education/formacoes')):
    if not fn.endswith('.html') or fn in ('index.html', 'formacao-corretor-imoveis-litoral.html'): continue
    p = f'education/formacoes/{fn}'
    t = open(p, encoding='utf-8').read()
    m = re.search(r'(<h2>Conte\u00fado principal</h2>\s*)<ul>(.*?)</ul>', t, flags=re.S)
    if not m:
        report["skipped"].append(fn); continue
    items = re.findall(r'<li>(.*?)</li>', m.group(2), flags=re.S)
    rows = ''.join(f'<tr><td>{i+1}</td><td>{esc(re.sub("<[^>]+>","",it))}</td></tr>' for i, it in enumerate(items))
    table = m.group(1) + f'<table><tr><th>#</th><th>T\u00f3pico coberto</th></tr>{rows}</table>'
    t = t[:m.start()] + table + t[m.end():]
    if '</style>' in t and 'th{background:#0077B6' not in t:
        t = t.replace('</style>', STYLE + '</style>', 1)
    open(p, 'w', encoding='utf-8').write(t)
    report["formacoes"] += 1

print(json.dumps(report, ensure_ascii=False))
