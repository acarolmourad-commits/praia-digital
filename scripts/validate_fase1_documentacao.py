import csv, re, sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ROOT = Path('C:/Users/Carolina/praia-digital')
REPORT = ROOT / 'docs/editorial/fase1-validacao-documentacao-2026-08-17.md'
BASE_URL = 'https://praia.digital'

URLS = [
    'blog/escritura-registro-imovel-litoral-passo-passo-2026.html',
    'blog/escritura-imovel-litoral-passos-custos-2026.html',
    'blog/financiamento-imoveis-litoral-guia.html',
    'blog/financiamento-imobiliario-litoral-guia-2026.html',
    'blog/financiamento-imoveis-litoral-paulista-guia-2026.html',
    'blog/avaliacao-preco-imoveis-litoral.html',
    'blog/avaliacao-preco-mercado-litoral.html',
    'blog/documentacao-compra-imovel-litoral-guia-2026.html',
    'blog/documentos-essenciais-compra-imovel-litoral-2026.html',
]

def check_remote(rel):
    url = f"{BASE_URL}/{rel}"
    try:
        req = Request(url, headers={'User-Agent':'Mozilla/5.0'})
        with urlopen(req, timeout=15) as r:
            return r.status, r.headers.get('content-type',''), r.read(200).decode('utf-8', errors='ignore')
    except HTTPError as e:
        return e.code, '', ''
    except Exception:
        return None, '', ''

def check_local(rel):
    p = ROOT / rel
    if not p.exists():
        return None, ''
    txt = p.read_text(encoding='utf-8', errors='ignore')
    title = re.search(r'<title[^>]*>(.*?)</title>', txt, re.I|re.S)
    title = title.group(1).strip() if title else ''
    meta = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', txt, re.I)
    meta = meta.group(1).strip() if meta else ''
    canonical = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', txt, re.I)
    canonical = canonical.group(1).strip() if canonical else ''
    ga = 'GA4_MEASUREMENT_ID' in txt or 'googletagmanager' in txt.lower()
    return len(txt), {'title': title, 'meta': meta, 'canonical': canonical, 'ga': ga}

def main():
    rows = []
    for rel in URLS:
        status, ctype, head = check_remote(rel)
        size, local = check_local(rel)
        rows.append({
            'url': rel,
            'http_status': status if status is not None else 'UNREACHABLE',
            'content_type': ctype,
            'local_exists': 'YES' if size is not None else 'NO',
            'local_size': size or 0,
            'title': local.get('title','') if local else '',
            'meta': local.get('meta','') if local else '',
            'canonical': local.get('canonical','') if local else '',
            'ga': 'YES' if local and local.get('ga') else 'NO',
        })

    lines = [
        '# Validação Fase 1 — Documentação Imobiliária',
        'Data: 2026-08-17',
        'Ações aplicadas: NENHUMA; somente validação.',
        '',
        '| URL | HTTP | Local | Tamanho | Title | Canonical | GA |',
        '|---|---|---|---|---|---|---|',
    ]
    for r in rows:
        lines.append(f"| {r['url']} | {r['http_status']} | {r['local_exists']} | {r['local_size']} | {r['title'][:60]} | {r['canonical'][:60]} | {r['ga']} |")
    lines += ['','Arquivos validados sem alteração.','']
    REPORT.write_text('\n'.join(lines), encoding='utf-8')
    print('report', REPORT)
    print('done', len(rows))

if __name__ == '__main__':
    main()
