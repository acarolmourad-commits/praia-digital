import os, re

def fix(path):
    name = path.split('/')[-1]
    expected = 'https://praia.digital/blog/' + name
    t = open(path, encoding='utf-8').read()
    if not re.search(r"rel=['\"]canonical['\"]", t, re.I):
        return False
    t2 = re.sub(r"[ \t]*<link[^>]*?rel=['\"]canonical['\"][^>]*?>\s*\n?", '', t, flags=re.I)
    def add(m):
        return m.group(1) + '  <link rel="canonical" href="' + expected + '">' + '\n'
    t2 = re.sub(r'(<head>\s*\n)', add, t2, count=1, flags=re.I)
    if t2 != t:
        open(path, 'w', encoding='utf-8').write(t2)
        return True
    return False

def needs_fix(path):
    name = path.split('/')[-1]
    expected = 'https://praia.digital/blog/' + name
    t = open(path, encoding='utf-8', errors='replace').read()
    cans = re.findall(r"<link[^>]*?rel=['\"]canonical['\"][^>]*?>", t, re.I)
    hrefs = []
    for c in cans:
        m = re.search(r"href=['\"]([^'\"]+)['\"]", c)
        hrefs.append(m.group(1) if m else None)
    return len(cans) > 1 or (cans and expected not in hrefs)

changed = []
for f in sorted(os.listdir('blog')):
    if not f.endswith('.html'):
        continue
    p = 'blog/' + f
    try:
        if needs_fix(p) and fix(p):
            changed.append(p)
    except Exception as e:
        print('ERRO', p, e)
print('corrigidos:', len(changed))
for c in changed:
    print(c)
