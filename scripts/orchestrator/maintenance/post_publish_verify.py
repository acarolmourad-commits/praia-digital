#!/usr/bin/env python3
"""
Verificação pós-publicação do orchestrator.
Checa se o resultado esperado realmente aconteceu após publicar.
Não altera conteúdo; apenas registra divergências para correção no próximo ciclo.
"""
import json, re, sys
from pathlib import Path
from datetime import datetime, timezone

REPO = Path('.').resolve()
BLOG_DIR = REPO / 'blog'
SITEMAP_PATH = REPO / 'sitemap.xml'
REGISTRY = REPO / 'docs' / 'banco-editorial.json'
VERIFICATION_LOG = REPO / 'docs' / 'orchestrator_verification.json'

MIN_CONTENT_SIZE = 800
MIN_INTERNAL_LINKS = 1
REQUIRED_CTA_PATTERNS = ['whatsapp', 'wa.me', 'comprar', 'checkout']


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as e:
        print(f'failed to load {path}: {e}')
        sys.exit(2)


def load_sitemap_slugs() -> set:
    if not SITEMAP_PATH.exists():
        return set()
    txt = SITEMAP_PATH.read_text(encoding='utf-8', errors='ignore')
    urls = set(re.findall(r'<loc>(.*?)</loc>', txt))
    slugs = set()
    for url in urls:
        if '/blog/' in url and url.endswith('.html'):
            slugs.add(Path(url).stem)
        elif '/noticias/' in url and url.endswith('.html'):
            slugs.add(Path(url).stem)
    return slugs


def verify_article(html_path: Path, sitemap_slugs: set) -> dict:
    if not html_path.exists():
        return {'valid': False, 'error': 'missing', 'issues': ['file_missing']}

    txt = html_path.read_text(encoding='utf-8', errors='ignore')
    slug = html_path.stem
    issues = []

    # Skip redirect stubs: they are not publishable content
    is_redirect = (
        re.search(r'<title[^>]*>(.*?)</title>', txt, re.S|re.I) and
        'redirecionando' in re.search(r'<title[^>]*>(.*?)</title>', txt, re.S|re.I).group(1).lower()
    ) or bool(re.search(r'<meta[^>]+http-equiv=["\']refresh["\']', txt, re.I))
    if is_redirect:
        return {'slug': slug, 'file': html_path.name, 'valid': True, 'issues': [], 'size': len(txt), 'internal_links': 0, 'in_sitemap': True, 'has_cta': False, 'skipped': True}

    # 1. Exists in sitemap
    in_sitemap = slug in sitemap_slugs
    if not in_sitemap:
        issues.append('missing_from_sitemap')

    # 2. Internal links
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', txt, re.I)
    domain = 'praia.digital'
    internal = []
    for h in hrefs:
        if h.startswith(('/blog/', '/education/', '/noticias/', 'blog/', 'education/', 'noticias/')):
            internal.append(h)
            continue
        if h.startswith(('http://', 'https://', '//', '#', 'mailto:', 'tel:')):
            if domain in h:
                internal.append(h)
            continue
        if h.endswith('.html') or h.endswith('.htm'):
            internal.append(h)
    if len(internal) < MIN_INTERNAL_LINKS:
        issues.append(f'insufficient_internal_links:{len(internal)}')

    # 3. CTA/WhatsApp
    has_cta = any(p in txt.lower() for p in REQUIRED_CTA_PATTERNS)
    if not has_cta:
        issues.append('missing_cta_or_whatsapp')

    # 4. Content size
    if len(txt) < MIN_CONTENT_SIZE:
        issues.append(f'content_too_small:{len(txt)}')

    # 5. Basic SEO
    if '<title>' not in txt.lower():
        issues.append('missing_title')
    if 'meta name="description"' not in txt.lower():
        issues.append('missing_description')
    if '<h1' not in txt.lower():
        issues.append('missing_h1')

    return {
        'slug': slug,
        'file': html_path.name,
        'valid': len(issues) == 0,
        'issues': issues,
        'size': len(txt),
        'internal_links': len(internal),
        'in_sitemap': in_sitemap,
        'has_cta': has_cta,
    }


def verify_latest_articles(limit: int = 10) -> dict:
    if not BLOG_DIR.exists():
        return {'status': 'error', 'message': 'blog dir missing'}

    sitemap_slugs = load_sitemap_slugs()
    files = sorted(BLOG_DIR.glob('*.html'), key=lambda p: p.stat().st_mtime, reverse=True)[:limit]
    results = []
    for f in files:
        results.append(verify_article(f, sitemap_slugs))

    failed = [r for r in results if not r.get('valid')]
    return {
        'status': 'ok',
        'checked': len(results),
        'failed': len(failed),
        'results': results,
        'failed_slugs': [r['slug'] for r in failed],
    }


def append_to_registry(verification: dict) -> dict:
    try:
        registry = load_json(REGISTRY)
    except Exception:
        registry = {}

    if 'orchestrator_verification' not in registry:
        registry['orchestrator_verification'] = []

    entry = {
        'date': datetime.now(timezone.utc).isoformat(),
        'checked': verification.get('checked', 0),
        'failed': verification.get('failed', 0),
        'failed_slugs': verification.get('failed_slugs', []),
        'results': verification.get('results', []),
    }
    registry['orchestrator_verification'].append(entry)
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')
    return {'status': 'ok', 'registered': True}


def save_verification_log(verification: dict) -> None:
    VERIFICATION_LOG.write_text(
        json.dumps(verification, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )


def main() -> dict:
    verification = verify_latest_articles(limit=10)
    save_verification_log(verification)
    append_to_registry(verification)

    failed_slugs = verification.get('failed_slugs', [])
    if failed_slugs:
        print(f"VERIFICATION: {verification['failed']}/{verification['checked']} articles failed checks")
        for slug in failed_slugs[:10]:
            print(f"  - {slug}")
        return {'status': 'divergences_found', 'failed': verification['failed'], 'failed_slugs': failed_slugs}

    print(f"VERIFICATION: {verification['checked']} articles OK")
    return {'status': 'ok', 'checked': verification['checked']}


if __name__ == '__main__':
    result = main()
    sys.exit(0 if result.get('status') == 'ok' else 1)
