#!/usr/bin/env python3
"""Inspect local references; optionally sample public external URLs once a week.

Findings are advisory, not a deployment gate. HTTP results never enter the
legacy internal-link/year issue consumed by Site Fixer. Importing is inert.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import datetime
from html.parser import HTMLParser
import ipaddress
import json
import os
from pathlib import Path
import re
import socket
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urljoin, urlsplit, urlunsplit
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://praia.digital/'
ATTRIBUTES = {'href', 'src', 'poster', 'cite', 'action', 'formaction'}
YEAR_RE = re.compile(r'\b(20(?:19|20|21|22|23|24|25))\b')
MAX_EXTERNAL, WORKERS, TIMEOUT = 80, 4, 12
DETAIL_LIMIT = 200


class References(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.links, self.base = [], None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'base':
            if self.base is None and 'href' in values:
                self.base = values['href']
            return
        self.links.extend((name, value) for name, value in attrs
                          if name in ATTRIBUTES and value is not None)


def reference(value, page, base=None):
    """Resolve URL syntax without network access; anchors alone are not checked."""
    value = value.strip()
    if not value or value.startswith('#'):
        return 'ignored', 'empty_or_anchor'
    if '${' in value or '{{' in value or '<%' in value:
        return 'ignored', 'template'
    try:
        origin = urljoin(ORIGIN, quote(page, safe='/'))
        url = urlsplit(urljoin(urljoin(origin, base or ''), value))
        if url.scheme not in ('http', 'https'):
            return 'ignored', 'non_http_scheme'
        if not url.hostname or url.username is not None or url.password is not None:
            return 'ignored', 'invalid_or_credential_url'
        if url.port not in (None, 80, 443):
            return 'ignored', 'nonstandard_port'
        if url.hostname in ('praia.digital', 'www.praia.digital'):
            return 'internal', unquote(url.path)
        host = url.hostname.encode('idna').decode('ascii').lower()
        if ':' in host:
            host = '[' + host + ']'
        if url.port is not None and url.port != (443 if url.scheme == 'https' else 80):
            host += ':' + str(url.port)
        normalized = urlunsplit((url.scheme, host, url.path or '/', url.query, ''))
        return 'external', quote(normalized, safe=":/?[]@!$&'()*+,;=%")
    except ValueError:
        return 'ignored', 'invalid_url'


def local_exists(path, root):
    """Offline lookup, including the existing extensionless-page convention."""
    if '\x00' in path or '\\' in path:
        return False
    root = Path(root).resolve()
    target = (root / path.lstrip('/')).resolve()
    if not target.is_relative_to(root):
        return False
    candidates = [target / 'index.html'] if path.endswith('/') else [
        target, Path(str(target) + '.html'), target / 'index.html']
    return any(p.resolve().is_relative_to(root) and p.is_file() for p in candidates)


def scan(root=ROOT):
    root = Path(root).resolve()
    broken, outdated, errors, external = [], [], [], {}
    counts, ignored = Counter(), Counter()
    for page in sorted(root.rglob('*.html')):
        rel = page.relative_to(root).as_posix()
        if any(p.startswith('.') or p == 'node_modules' for p in page.relative_to(root).parts):
            continue
        if rel.startswith('social/'):
            continue
        if not page.resolve().is_relative_to(root):
            errors.append({'page': rel, 'error': 'outside_root'})
            continue
        try:
            text = page.read_text(encoding='utf-8', errors='replace')
        except OSError as exc:
            errors.append({'page': rel, 'error': type(exc).__name__})
            continue
        counts['pages_scanned'] += 1
        parser = References(text)
        for attr, value in parser.links:
            counts['references_extracted'] += 1
            kind, target = reference(value, rel, parser.base)
            if kind == 'ignored':
                ignored[target] += 1
            elif kind == 'external' and attr in ('action', 'formaction'):
                ignored['external_form_endpoint'] += 1
            elif kind == 'external':
                counts['external_references'] += 1
                external.setdefault(target, {'page': rel, 'attribute': attr})
            else:
                counts['internal_checked'] += 1
                if not local_exists(target, root):
                    broken.append({'page': rel, 'link': value, 'attribute': attr})
        # Preserve the legacy year findings, separate from HTTP findings.
        for segment in re.findall(r'>([^<>]+)<', text):
            for match in YEAR_RE.finditer(segment):
                context = segment[max(0, match.start()-40):match.end()+40].strip()
                outdated.append({'page': rel, 'year': match.group(1), 'context': context[:120]})
    return counts, ignored, broken, outdated, errors, external


def weekly_sample(urls, day, limit=MAX_EXTERNAL):
    """Rotate batches; full coverage needs ceil(N/limit) stable weeks."""
    urls = sorted(set(urls))
    if not urls:
        return []
    limit = min(MAX_EXTERNAL, max(1, limit))
    batches = (len(urls) + limit - 1) // limit
    week = (day - datetime.date(1970, 1, 5)).days // 7
    start = (week % batches) * limit
    return urls[start:start + limit]


def public_url(url):
    """Reject local/credential URLs, including redirect destinations."""
    parts = urlsplit(url)
    if parts.scheme not in ('http', 'https') or not parts.hostname:
        raise ValueError('unsupported_url')
    if parts.username is not None or parts.password is not None or parts.port not in (None, 80, 443):
        raise ValueError('unsupported_url')
    addresses = socket.getaddrinfo(parts.hostname, parts.port or (443 if parts.scheme == 'https' else 80),
                                   type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(entry[4][0]).is_global for entry in addresses):
        raise ValueError('non_public_destination')


class PublicRedirects(urllib.request.HTTPRedirectHandler):
    max_redirections = 3

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        public_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def classify_status(status, redirected=False):
    if status in (404, 410):
        return 'broken'
    if status in (401, 403, 429):
        return 'restricted'
    if status == 408 or status >= 500:
        return 'transient'
    if 200 <= status < 300:
        return 'redirect' if redirected else 'ok'
    if 300 <= status < 400:
        return 'redirect'
    return 'review'


def check_external(url):
    result = {'url': url}
    try:
        public_url(url)
        opener = urllib.request.build_opener(PublicRedirects())
        headers = {'User-Agent': 'PraiaDigitalLinkInspector/1.0 (+https://praia.digital/)'}
        for method in ('HEAD', 'GET'):
            try:
                req = urllib.request.Request(url, headers=headers, method=method)
                with opener.open(req, timeout=TIMEOUT) as response:
                    status, final = response.status, response.geturl()
                break  # Do not read the response body.
            except HTTPError as exc:
                status, final = exc.code, exc.geturl()
                exc.close()
                if method == 'HEAD' and status in (405, 501):
                    continue
                break
        result.update(status=status, final_url=final, redirected=final != url,
                      category=classify_status(status, final != url), method=method)
    except ValueError as exc:
        result.update(category='not_checked', reason=str(exc))
    except (URLError, OSError) as exc:
        result.update(category='transient', reason=type(exc).__name__)
    return result


def external_report(urls, enabled, day):
    selected = weekly_sample(urls, day) if enabled else []
    results = []
    if selected:
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            results = list(pool.map(check_external, selected))
        for result in results:
            result.update(urls[result['url']])
    checked = sum('status' in result for result in results)
    totals = dict(Counter(result['category'] for result in results))
    return {'enabled': enabled, 'unique_candidates': len(urls), 'selected': len(selected),
            'http_responses': checked, 'pending': len(urls) - len(selected),
            'selected_without_response': len(selected) - checked,
            'max_per_run': MAX_EXTERNAL, 'rotation_week': day.strftime('%G-W%V'),
            'status': 'not_run' if not enabled else ('no_candidates' if not urls else 'sampled'),
            'categories': totals, 'results': results,
            'coverage_note': 'Amostra rotativa; URLs pendentes e sem resposta nao foram validadas. '
                             'Nao verifica JavaScript, formularios, ancoras ou todo o site publicado.'}


def md_section(title, items, fmt):
    if not items:
        return f'### {title}\n\nNenhum problema encontrado. ✅\n'
    lines = [f'### {title} ({len(items)})\n'] + [fmt(it) for it in items[:50]]
    if len(items) > 50:
        lines.append(f'- ... e mais {len(items)-50} ocorrencias')
    return '\n'.join(lines) + '\n'


def issue_body(day, pages, broken, outdated):
    # No external result parameter: Site Fixer only sees legacy findings.
    return (f'## Relatorio de Inspecao — {day}\n\nPaginas inspecionadas: **{pages}**\n\n'
            + md_section('Links internos quebrados', broken,
                         lambda b: f"- `{b['page']}` → link `{b['link']}`")
            + '\n' + md_section('Mencoes a anos anteriores — revisar contexto, sem presumir erro', outdated,
                                lambda o: f"- `{o['page']}` menciona **{o['year']}**: \"...{o['context']}...\"")
            + '\n---\nGerado pelo agente **site-inspector**. Verificacao local; '
              'ocorrencias requerem revisao, nao reescrita automatica. '
              'Resultados HTTP externos ficam somente no artefato.\n')


def publish_issue(day, pages, broken, outdated):
    token = os.environ.get('GITHUB_TOKEN', '')
    if not token or not (broken or outdated):
        return
    repo = os.environ.get('GITHUB_REPOSITORY', 'acarolmourad-commits/praia-digital')

    def gh(method, path, payload=None):
        req = urllib.request.Request(
            f'https://api.github.com/repos/{repo}{path}',
            data=json.dumps(payload).encode() if payload is not None else None,
            headers={'Authorization': f'Bearer {token}', 'Accept': 'application/vnd.github+json',
                     'Content-Type': 'application/json'}, method=method)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            return json.loads(response.read() or b'{}')

    issues = gh('GET', '/issues?state=open&labels=site-inspection&per_page=5')
    existing = next((i for i in issues if i['title'].startswith('[Site Inspector]')), None)
    payload = {'title': f'[Site Inspector] Relatorio {day}',
               'body': issue_body(day, pages, broken, outdated)}
    if existing:
        gh('PATCH', f"/issues/{existing['number']}", payload)
        print('ISSUE ATUALIZADA:', existing['number'])
    else:
        payload['labels'] = ['site-inspection']
        created = gh('POST', '/issues', payload)
        print('ISSUE CRIADA:', created['number'])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--external', action='store_true', help='Opt-in bounded HTTP sample')
    parser.add_argument('--no-publish', action='store_true', help='Do not create/update issues')
    args = parser.parse_args(argv)
    day = datetime.datetime.now(datetime.timezone.utc).date()
    counts, ignored, broken, outdated, errors, urls = scan(args.root)
    external = external_report(urls, args.external, day)
    coverage_ok = bool(counts['pages_scanned'] and counts['references_extracted']) and not errors
    report = {'date': day.isoformat(), **dict(counts), 'ignored': dict(ignored),
              'broken_links': broken[:DETAIL_LIMIT], 'outdated_mentions': outdated[:DETAIL_LIMIT],
              'totals': {'broken': len(broken), 'outdated': len(outdated)},
              'read_errors': errors[:DETAIL_LIMIT], 'read_error_count': len(errors),
              'coverage_ok': coverage_ok, 'external': external,
              'advisory': True, 'detail_limit': DETAIL_LIMIT}
    (args.root / 'site_inspection_report.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    summary = (f"RESUMO: {counts['pages_scanned']} paginas | {counts['references_extracted']} referencias | "
               f"{len(broken)} links locais para revisao | {len(outdated)} mencoes de anos\n"
               f"HTTP: {external['status']} | {external['http_responses']} respostas | "
               f"{external['pending']} pendentes | {external['selected_without_response']} selecionadas sem resposta\n"
               f"Categorias HTTP: {json.dumps(external['categories'], ensure_ascii=False)}\n"
               f"Cobertura de leitura: {'completa' if coverage_ok else 'INCOMPLETA'}; "
               'conclusao do job nao significa ausencia de links quebrados.\n')
    print(summary)
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8') as handle:
            handle.write('### Site Inspector\n\n' + summary.replace('\n', '\n\n'))
    if not args.no_publish and coverage_ok:
        publish_issue(day, counts['pages_scanned'], broken, outdated)
    return 0 if coverage_ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
