#!/usr/bin/env python3
"""Padroniza tags Google (title, description, canonical, OG, H1, schema) em todas as paginas HTML.
Conservador: apenas INSERE tags ausentes; nunca altera conteudo existente. Idempotente."""
import os, re, html, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCL = ('/backup', '/backups', '/.git', 'node_modules', 'docs/seo/tmp_adversarial')

def esc(s): return html.escape(s.strip(), quote=True)

def slug_title(rel):
    name = os.path.basename(rel).replace('.html','').replace('-',' ').replace('_',' ')
    return name.strip().capitalize() + ' — Praia Digital'

def fix(fp, rel):
    t = open(fp, encoding='utf-8', errors='ignore').read()
    orig = t
    if '<html' not in t.lower() and not re.search(r'<!DOCTYPE html', t, re.I):
        return False
    url = 'https://praia.digital/' + rel
    m = re.search(r'<title>([^<]+)</title>', t, re.I); title_txt = m.group(1).strip() if m else None
    m = re.search(r'<h1[^>]*>(.*?)</h1>', t, re.I|re.S)
    h1_txt = re.sub(r'<[^>]+>','',m.group(1)).strip() if m else None
    m = re.search(r'name="description"\s+content="([^"]+)"', t, re.I)
    desc_txt = m.group(1).strip() if m else None
    base_title = title_txt or h1_txt or slug_title(rel)
    base_desc = desc_txt or base_title
    inject = []
    if not re.search(r'<html[^>]*lang=', t, re.I):
        t = re.sub(r'<html', '<html lang="pt-BR"', t, count=1, flags=re.I)
    if not re.search(r'<!DOCTYPE html', t, re.I):
        t = '<!DOCTYPE html>\n' + t
    if not re.search(r'charset=', t, re.I):
        inject.append('<meta charset="UTF-8">')
    if not re.search(r'name="viewport"', t, re.I):
        inject.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    if not title_txt:
        inject.append('<title>%s</title>' % esc(base_title))
    if not desc_txt:
        inject.append('<meta name="description" content="%s">' % esc(base_desc))
    if not re.search(r'rel="canonical"', t, re.I):
        inject.append('<link rel="canonical" href="%s">' % url)
    if not re.search(r'application/ld\+json', t, re.I):
        ld = json.dumps({"@context":"https://schema.org","@type":"WebPage","name":base_title,
                         "description":base_desc,"url":url}, ensure_ascii=False)
        inject.append('<script type="application/ld+json">%s</script>' % ld)
    if 'property="og:' not in t:
        inject.append('<meta property="og:type" content="website">\n'
                      '<meta property="og:title" content="%s">\n'
                      '<meta property="og:description" content="%s">\n'
                      '<meta property="og:url" content="%s">\n'
                      '<meta property="og:image" content="https://praia.digital/img/default-home.jpg">'
                      % (esc(base_title), esc(base_desc), url))
    if inject:
        he = re.search(r'</head>', t, re.I)
        if he:
            t = t[:he.start()] + '\n'.join(inject) + '\n' + t[he.start():]
        else:
            m2 = re.search(r'<html[^>]*>', t, re.I)
            if not m2: return False
            t = t[:m2.end()] + '\n<head>\n' + '\n'.join(inject) + '\n</head>\n' + t[m2.end():]
    if not re.search(r'<h1[\s>]', t, re.I):
        h1tag = '\n<h1>%s</h1>' % esc(base_title)
        body = re.search(r'<body[^>]*>', t, re.I)
        he = re.search(r'</head>', t, re.I)
        if body: t = t[:body.end()] + h1tag + t[body.end():]
        elif he: t = t[:he.end()] + h1tag + t[he.end():]
        else: return False
    if t != orig:
        open(fp, 'w', encoding='utf-8').write(t)
        return True
    return False

changed = 0
for dp, dn, fn in os.walk(ROOT):
    rel_dir = dp.replace(ROOT, '')
    if any(x in rel_dir for x in EXCL): continue
    for f in fn:
        if not f.endswith('.html'): continue
        fp = os.path.join(dp, f)
        rel = os.path.relpath(fp, ROOT).replace(os.sep, '/')
        try:
            if fix(fp, rel): changed += 1
        except Exception as e:
            print('skip', rel, e, file=sys.stderr)
print('arquivos corrigidos:', changed)
