import glob
import re

patterns = [
    re.compile(r'<img src="([^"]+)" <img  (alt="[^"]+")>'),
    re.compile(r'<img src="([^"]+)"<img  (alt="[^"]+")>'),
    re.compile(r'<img  (alt="[^"]+") <img src="([^"]+)">'),
]

fixed = 0
for path in glob.glob('imoveis/imovel-*.html') + glob.glob('imoveis/imoveis/*.html'):
    txt = open(path, 'r', encoding='utf-8', errors='ignore').read()
    original = txt
    for pat in patterns:
        def repl(m):
            groups = m.groups()
            if 'src=' in m.group(0) and groups[0].startswith('http'):
                return f'<img src="{groups[0]}" {groups[1]}>'
            else:
                return f'<img {groups[0]} src="{groups[1]}>'
        txt = pat.sub(repl, txt)
    if txt != original:
        open(path, 'w', encoding='utf-8').write(txt)
        fixed += 1

print('fixed', fixed)
