import os, re, json
MAP = {
    '#0b1220': '#F4EBD0',  # fundo navy -> areia
    '#e8ecf1': '#023047',  # texto claro -> azul escuro
    '#cfe3ff': '#023047',  # texto azul claro -> azul escuro
    '#0b2d4d': '#f8fafc',  # card escuro -> claro
    '#94a3b8': '#41525f',  # cinza fraco -> cinza legivel
    '#58a6ff': '#0077B6',  # link azul claro -> oceano
    '#0ea5e9': '#0077B6',  # link ciano -> oceano
}
pat = re.compile('|'.join(re.escape(k) for k in MAP), re.I)
changed = []
for root, dirs, files in os.walk('education'):
    dirs[:] = [d for d in dirs if d != '.git']
    for fn in files:
        if not fn.endswith('.html'): continue
        p = os.path.join(root, fn)
        try: t = open(p, encoding='utf-8').read()
        except Exception: continue
        if not re.search(r'#(0b1220|e8ecf1|cfe3ff|0b2d4d|94a3b8|58a6ff|0ea5e9)', t, re.I): continue
        nt = pat.sub(lambda m: MAP[m.group(0).lower()], t)
        if nt != t:
            open(p, 'w', encoding='utf-8').write(nt)
            changed.append(p)
print(json.dumps({"files_changed": len(changed)}))
