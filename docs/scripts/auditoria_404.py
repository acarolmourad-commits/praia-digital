#!/usr/bin/env python3
"""
Auditoria de 404 — Praia Digital
Gera relatório de links/páginas quebradas sem alterar arquivos.
"""
import csv, re, sys
from pathlib import Path
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

BASE = Path(__file__).resolve().parent.parent.parent
BLOG_DIR = BASE / 'blog'
SITEMAP_PATH = BASE / 'sitemap.xml'
REPORT_PATH = BASE / 'docs' / 'comercial' / 'auditoria_404_2026-08-18.csv'
MAX_WORKERS = 12
TIMEOUT = 15

HEADERS = {'User-Agent': 'Mozilla/5.0 (PraiaDigital/1.0; +https://praia.digital)'}


def extract_urls_from_html(content: str, base_url: str):
    urls = []
    for m in re.finditer(r'href=["\'](.*?)["\']', content, flags=re.IGNORECASE):
        u = m.group(1).strip()
        if u.startswith('#') or u.startswith('mailto:') or u.startswith('tel:'):
            continue
        if u.startswith('//'):
            u = 'https:' + u
        if not urlparse(u).scheme:
            u = urljoin(base_url, u)
        urls.append(u)
    return urls


def extract_urls_from_sitemap(content: str):
    urls = []
    for m in re.finditer(r'<loc>(.*?)</loc>', content, flags=re.IGNORECASE | re.DOTALL):
        u = m.group(1).strip()
        if u:
            urls.append(u)
    return urls


def check_url(url: str):
    try:
        r = requests.head(url, allow_redirects=True, timeout=TIMEOUT, headers=HEADERS)
        if r.status_code >= 400:
            return url, r.status_code
        return url, None
    except requests.RequestException as e:
        return url, str(e)


def main():
    print('Iniciando auditoria de 404...')
    internal_urls = set()
    for p in BLOG_DIR.glob('*.html'):
        try:
            content = p.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        base_url = f'https://praia.digital/blog/{p.name}'
        for u in extract_urls_from_html(content, base_url):
            if 'praia.digital' in u:
                internal_urls.add(u.split('#')[0])

    sitemap_urls = []
    if SITEMAP_PATH.exists():
        sitemap_urls = extract_urls_from_sitemap(SITEMAP_PATH.read_text(encoding='utf-8', errors='ignore'))
        internal_urls.update(sitemap_urls)

    print(f'URLs internas coletadas: {len(internal_urls)}')
    print(f'URLs no sitemap: {len(sitemap_urls)}')

    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(check_url, u): u for u in internal_urls}
        for fut in as_completed(futures):
            url, status = fut.result()
            if status:
                results.append((url, status))

    results.sort()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with REPORT_PATH.open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['url', 'status'])
        for row in results:
            writer.writerow(row)
    print(f'Relatório gerado: {REPORT_PATH}')
    print(f'Total de falhas: {len(results)}')
    if results:
        print('Primeiras 20:')
        for row in results[:20]:
            print(' ', row)
    return results


if __name__ == '__main__':
    main()
