#!/usr/bin/env python3
"""Subagente Site Fixer (praia.digital).
Acionado pelo site-inspector (issue com label 'site-inspection' ou dispatch).
Correcoes automaticas seguras:
1. Links internos quebrados que resolvem com .html ou /index.html -> reescrita.
2. Mencoes a anos antigos (<= ano anterior) em texto visivel -> ano corrente
   (conteudo datado em blog/ nao e alterado).
Commita as correcoes e comenta na issue de origem.
Fix 2026-10-06: nao falha quando nao ha mudancas reais (git commit vazio)
e so contabiliza correcao quando o link de fato muda."""
import os, re, json, glob, datetime, subprocess, urllib.request

TOKEN = os.environ.get('GITHUB_TOKEN','')
REPO = os.environ.get('GITHUB_REPOSITORY','acarolmourad-commits/praia-digital')
ISSUE = os.environ.get('ISSUE_NUMBER','')
CURRENT_YEAR = str(datetime.date.today().year)
OLD_YEARS = re.compile(r'\b(20(?:19|20|21|22|23|24|25))\b')
LINK_RE = re.compile(r'((?:href|src)=["\'])([^"\']+)(["\'])')
SKIP_PREFIX = ('http://','https://','mailto:','tel:','#','javascript:','data:')

HTML = [f for f in glob.glob('**/*.html', recursive=True)
        if not f.startswith(('node_modules/', '.git/', 'social/'))]

def run(cmd): subprocess.run(cmd, shell=True, check=True)

def resolve_variants(src, base):
    p = src.split('#')[0].split('?')[0]
    suffix = src[len(p):]
    if not p: return None
    cand = p.lstrip('/') if p.startswith('/') else os.path.normpath(os.path.join(os.path.dirname(base), p))
    if os.path.exists(cand): return None  # nao esta quebrado
    if os.path.exists(cand + '.html'):
        new = p + '.html'
        return ('/' + new if p.startswith('/') else new) + suffix
    idx = os.path.join(cand, 'index.html')
    if os.path.exists(idx):
        new = p.rstrip('/') + '/'
        return ('/' + new if p.startswith('/') else new) + suffix
    return False  # quebrado sem correcao segura

fix_links, fix_years, skipped = [], [], []
for f in HTML:
    txt = open(f, encoding='utf-8', errors='ignore').read()
    orig = txt
    # 1) links
    def repl(m):
        pre, u, pos = m.groups()
        if u.startswith(SKIP_PREFIX): return m.group(0)
        v = resolve_variants(u, f)
        if v and v != u:  # so conta se o link de fato muda
            fix_links.append({'page': f, 'from': u, 'to': v})
            return pre + v + pos
        if v is False:
            skipped.append({'page': f, 'link': u})
        return m.group(0)
    txt = LINK_RE.sub(repl, txt)
    # 2) anos antigos em texto visivel (blog/ e conteudo datado: nao alterar)
    if f.startswith('blog/'):
        if txt != orig:
            open(f, 'w', encoding='utf-8').write(txt)
        continue
    def repl_year(m):
        seg = m.group(0)
        if not OLD_YEARS.search(seg): return seg
        inner = seg[1:-1]
        new = OLD_YEARS.sub(CURRENT_YEAR, inner)
        fix_years.append({'page': f, 'before': inner.strip()[:80], 'after': new.strip()[:80]})
        return '>' + new + '<'
    txt = re.sub(r'>[^<>]+<', repl_year, txt)
    if txt != orig:
        open(f, 'w', encoding='utf-8').write(txt)

def gh(method, path, payload=None):
    req = urllib.request.Request(
        f'https://api.github.com/repos/{REPO}{path}',
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={'Authorization': f'Bearer {TOKEN}', 'Accept': 'application/vnd.github+json',
                 'Content-Type': 'application/json'}, method=method)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read() or b'{}')

def has_changes():
    r = subprocess.run('git status --porcelain', shell=True, capture_output=True, text=True)
    return bool(r.stdout.strip())

if (fix_links or fix_years) and has_changes():
    run('git config user.name "github-actions[bot]"')
    run('git config user.email "github-actions[bot]@users.noreply.github.com"')
    run('git add -A')
    msg = f"fix(site): site-fixer - {len(fix_links)} links corrigidos, {len(fix_years)} mencoes atualizadas para {CURRENT_YEAR}"
    run(f'git commit -m "{msg}"')
    run('git push')
else:
    print('Nenhuma mudanca real no working tree - nada a commitar.')

summary = f"""### Correcoes aplicadas pelo subagente site-fixer

- **Links reescritos:** {len(fix_links)}
- **Mencoes de ano atualizadas para {CURRENT_YEAR}:** {len(fix_years)}
- **Links sem correcao segura (requer revisao manual):** {len(skipped)}
""" + ('\nLinks que precisam de revisao:\n' + '\n'.join(f"- `{s['page']}` → `{s['link']}`" for s in skipped[:30]) if skipped else '')

if TOKEN and ISSUE:
    gh('POST', f'/issues/{ISSUE}/comments', {'body': summary})
    print('COMENTARIO POSTADO na issue', ISSUE)
print(summary)
