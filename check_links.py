import os, re, json, sys
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = os.getcwd()
print('BASE:', BASE, flush=True)

html_files = []
for root, dirs, files in os.walk(BASE):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))
print(f'Total HTML: {len(html_files)}', flush=True)

href_pat = re.compile(r'(href|src|action|poster|cite|formaction)\s*=\s*([\"\'])(.*?)\\2', re.IGNORECASE)
broken_internal = []
all_externals = []
data_uri_count = 0
js_template_count = 0
seen_internal = set()
seen_external = set()

def normalize_target(base_dir, link):
    if not link:
        return None
    link = link.strip()
    if link.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'data:')):
        return None
    if re.search(r'\$\{|\+\s*(embedUrl|qrApi|filters)', link):
        return None
    if re.match(r'^https?://', link):
        return None
    if link.startswith('/'):
        return os.path.normpath(os.path.join(BASE, link[1:]))
    return os.path.normpath(os.path.join(base_dir, link))

for i, html_path in enumerate(html_files, 1):
    base_dir = os.path.dirname(html_path)
    try:
        with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception:
        continue
    for m in href_pat.finditer(content):
        attr, quote, link = m.groups()
        if not link:
            continue
        if link.startswith('data:'):
            data_uri_count += 1
            continue
        if link.startswith('javascript:'):
            continue
        if re.search(r'\$\{|\+\s*(embedUrl|qrApi|filters)', link):
            js_template_count += 1
            continue
        if re.match(r'^https?://', link):
            if link not in seen_external and len(all_externals) < 80:
                seen_external.add(link)
                all_externals.append(link)
            continue
        target = normalize_target(base_dir, link)
        if target is None or target.endswith('#'):
            continue
        rel = os.path.relpath(target, BASE)
        if not os.path.exists(target) and rel not in seen_internal:
            seen_internal.add(rel)
            broken_internal.append((os.path.relpath(html_path, BASE), attr, link, rel))
    if i % 500 == 0:
        print(f'  progresso: {i}/{len(html_files)}', flush=True)

print(f'\nData URIs: {data_uri_count}', flush=True)
print(f'JS/template refs ignorados: {js_template_count}', flush=True)
print(f'Links internos quebrados: {len(broken_internal)}', flush=True)
print(f'URLs externas unicas para checar: {len(all_externals)}', flush=True)

def check_url(url, timeout=12):
    try:
        req = Request(url, headers={'User-Agent':'Mozilla/5.0'})
        resp = urlopen(req, timeout=timeout)
        return url, resp.status
    except HTTPError as e:
        return url, e.code
    except URLError as e:
        return url, f'ERR:{e.reason}'
    except Exception as e:
        return url, f'ERR:{type(e).__name__}'

broken_external = []
if all_externals:
    print('Iniciando checagem externa...', flush=True)
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = {url: pool.submit(check_url, url) for url in all_externals}
        done = 0
        for fut in as_completed(futures.values()):
            done += 1
            if done % 20 == 0:
                print(f'  externos checados: {done}/{len(all_externals)}', flush=True)
            try:
                url, status = fut.result(timeout=20)
            except Exception:
                continue
            if status != 200:
                broken_external.append((url, status))

print(f'Links externos quebrados: {len(broken_external)}', flush=True)

print('\n=== INTERNOS QUEBRADOS ===', flush=True)
for b in broken_internal[:80]:
    print(f'  {b[0]} | attr={b[1]} | link={b[2]}\n    esperado: {b[3]}', flush=True)

print('\n=== EXTERNOS QUEBRADOS ===', flush=True)
for e in broken_external[:40]:
    print(f'  {e[1]} | URL={e[0]}', flush=True)

report = {
    'scanned': len(html_files),
    'data_uris': data_uri_count,
    'js_template_refs': js_template_count,
    'broken_internal': len(broken_internal),
    'broken_external': len(broken_external),
    'external_checked': len(all_externals),
    'external_ok': len(all_externals) - len(broken_external),
}
with open('link_check_report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
print('\nRelatorio salvo em link_check_report.json', flush=True)
