import os, re, json

MAP = {
    '#0d1117': '#F4EBD0',  # fundo escuro -> areia (design system)
    '#e6edf3': '#023047',  # texto claro -> azul escuro
    '#58a6ff': '#0077B6',  # links azul claro -> azul oceano
    '#161b22': '#f8fafc',  # cards/linhas escuras -> claro
    '#30363d': '#d0d7de',  # bordas escuras -> claras
    '#21262d': '#e5e7eb',  # fundos de barras -> claro
    '#1f6feb': '#0077B6',  # botoes/th azul github -> azul oceano
    '#d29922': '#F59E0B',  # amber escuro -> amber design system
}
pat = re.compile('|'.join(re.escape(k) for k in MAP), re.I)

changed = []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d != '.git']
    for fn in files:
        if not fn.endswith('.html'): continue
        p = os.path.join(root, fn)
        try: t = open(p, encoding='utf-8').read()
        except Exception: continue
        if '#0d1117' not in t.lower(): continue
        nt = pat.sub(lambda m: MAP[m.group(0).lower()], t)
        if nt != t:
            open(p, 'w', encoding='utf-8').write(nt)
            changed.append(p[2:])
print(json.dumps({"files_changed": len(changed)}))
