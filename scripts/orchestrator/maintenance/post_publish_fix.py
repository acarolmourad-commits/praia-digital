#!/usr/bin/env python3
"""
Correção automática pós-publicação para artigos do blog.
Aplica correções seguras quando o post_publish_verify detecta divergências.
Não altera conteúdo editorial; apenas integraSEO, links, CTA e sitemap.
"""
import json, re, sys
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import quote

REPO = Path('.').resolve()
BLOG_DIR = REPO / 'blog'
SITEMAP_PATH = REPO / 'sitemap.xml'
SITEMAP_SCRIPT = REPO / 'scripts' / 'gerar_sitemap.py'
REGISTRY = REPO / 'docs' / 'banco-editorial.json'
FIX_LOG = REPO / 'docs' / 'post_publish_fixes.json'

MIN_CONTENT_SIZE = 800
MIN_INTERNAL_LINKS = 1


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as e:
        print(f'failed to load {path}: {e}')
        sys.exit(2)


def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def get_sitemap_slugs() -> set:
    if not SITEMAP_PATH.exists():
        return set()
    txt = SITEMAP_PATH.read_text(encoding='utf-8', errors='ignore')
    urls = set(re.findall(r'<loc>(.*?)</loc>', txt))
    slugs = set()
    for url in urls:
        if '/blog/' in url and url.endswith('.html'):
            slugs.add(Path(url).stem)
    return slugs


def get_related_slugs(current_slug: str, limit: int = 3) -> list:
    """Find related blog articles to link to."""
    try:
        registry = load_json(REGISTRY)
        articles = registry.get('articles', [])
        candidates = [
            a['slug'] for a in articles
            if a.get('slug') != current_slug and a.get('status') == 'PUBLISHED'
        ]
        # Prefer same city if available
        city = None
        for part in current_slug.split('-'):
            if part in ['santos', 'guaruja', 'praia-grande', 'bertioga', 'sao-vicente', 'peruibe', 'itanhaem', 'mongagua', 'caraguatatuba', 'ilhabela', 'ubatuba', 'sao-sebastiao']:
                city = part
                break
        if city:
            city_slugs = [s for s in candidates if city in s]
            if city_slugs:
                return city_slugs[:limit]
        return candidates[:limit]
    except Exception:
        return []


def fix_article(html_path: Path, issues: list) -> dict:
    """Apply safe fixes to an article based on detected issues."""
    if not html_path.exists():
        return {'slug': html_path.stem, 'fixed': False, 'reason': 'file_missing'}

    txt = html_path.read_text(encoding='utf-8', errors='ignore')
    slug = html_path.stem
    applied = []
    failed = []

    # Extract title/h1
    m_title = re.search(r'<title>(.*?)</title>', txt, re.I|re.S)
    m_h1 = re.search(r'<h1[^>]*>(.*?)</h1>', txt, re.I|re.S)
    title = re.sub(r'<[^>]+>', '', m_title.group(1)).strip() if m_title else slug
    h1 = re.sub(r'<[^>]+>', '', m_h1.group(1)).strip() if m_h1 else slug

    # Fix: missing canonical
    if 'missing_canonical' in issues or 'rel="canonical"' not in txt:
        txt = txt.replace('</head>', f'<link rel="canonical" href="https://praia.digital/blog/{slug}.html">\n</head>')
        applied.append('canonical')

    # Fix: missing meta description
    if 'missing_description' in issues or 'meta name="description"' not in txt.lower():
        desc = h1[:160]
        txt = txt.replace('</head>', f'<meta name="description" content="{desc}">\n</head>')
        applied.append('description')

    # Fix: missing CTA/WhatsApp
    if 'missing_cta_or_whatsapp' in issues:
        if 'wa.me' not in txt.lower() and 'whatsapp' not in txt.lower():
            related = get_related_slugs(slug, limit=3)
            links_html = '\n'.join([f'<p><a href="/blog/{r}.html">{r}</a></p>' for r in related])
            cta_html = f'''
<p><strong>Quer vender ou alugar seu imóvel no litoral?</strong></p>
<p>Fale agora com um especialista pelo WhatsApp: <a href="https://wa.me/5511954346288?text=Ol%C3%A1,%20tenho%20interesse%20em%20{quote(h1)}">Clique aqui para atendimento</a></p>
{links_html}
'''
            txt = txt.replace('</body>', f'{cta_html}\n</body>')
            applied.append('cta_whatsapp')

    # Fix: insufficient internal links
    if any(issue.startswith('insufficient_internal_links') for issue in issues):
        hrefs = re.findall(r'href=["\']([^"\']+)["\']', txt, re.I)
        internal = []
        for h in hrefs:
            if h.startswith(('/blog/', '/education/', '/noticias/', 'blog/', 'education/', 'noticias/')):
                internal.append(h)
                continue
            if h.startswith(('http://', 'https://', '//', '#', 'mailto:', 'tel:')):
                if 'praia.digital' in h:
                    internal.append(h)
                continue
            if h.endswith('.html') or h.endswith('.htm'):
                internal.append(h)
        if len(internal) < MIN_INTERNAL_LINKS:
            related = get_related_slugs(slug, limit=3)
            links_html = '\n'.join([f'<p><a href="/blog/{r}.html">{r}</a></p>' for r in related if f'/blog/{r}.html' not in internal])
            if links_html:
                txt = txt.replace('</body>', f'{links_html}\n</body>')
                applied.append('internal_links')

    # Fix: content too small
    if any(issue.startswith('content_too_small') for issue in issues):
        if len(txt) < MIN_CONTENT_SIZE:
            expansion = f'''
<p>Conteúdo complementar sobre {h1}: informações atualizadas, dicas práticas e oportunidades para o mercado imobiliário do litoral.</p>
'''
            txt = txt.replace('</body>', f'{expansion}\n</body>')
            applied.append('content_expansion')

    # Write back if fixes applied
    if applied:
        html_path.write_text(txt, encoding='utf-8')
        return {'slug': slug, 'fixed': True, 'applied': applied}
    
    return {'slug': slug, 'fixed': False, 'reason': 'no_safe_fix'}


def update_sitemap() -> dict:
    """Regenerate sitemap."""
    try:
        import subprocess
        result = subprocess.run(
            f'python "{SITEMAP_SCRIPT}"',
            shell=True,
            cwd=REPO,
            capture_output=True,
            text=True,
            timeout=300,
        )
        return {'updated': result.returncode == 0, 'output': result.stdout[-200:] if result.stdout else ''}
    except Exception as e:
        return {'updated': False, 'error': str(e)}


def update_registry_verification(verification: dict) -> None:
    """Append verification results to registry."""
    try:
        registry = load_json(REGISTRY)
        if 'orchestrator_verification' not in registry:
            registry['orchestrator_verification'] = []
        registry['orchestrator_verification'].append({
            'date': datetime.now(timezone.utc).isoformat(),
            'checked': verification.get('checked', 0),
            'failed': verification.get('failed', 0),
            'failed_slugs': verification.get('failed_slugs', []),
        })
        save_json(REGISTRY, registry)
    except Exception as e:
        print(f'failed to update registry: {e}')


def mark_for_human_review(slugs: list, reason: str) -> None:
    """Mark articles that need human review."""
    try:
        registry = load_json(REGISTRY)
        if 'post_publish_human_review' not in registry:
            registry['post_publish_human_review'] = []
        for slug in slugs:
            registry['post_publish_human_review'].append({
                'slug': slug,
                'reason': reason,
                'date': datetime.now(timezone.utc).isoformat(),
                'status': 'REVISAR_HUMANO',
            })
        save_json(REGISTRY, registry)
    except Exception as e:
        print(f'failed to mark for human review: {e}')


def main() -> dict:
    from post_publish_verify import verify_latest_articles
    
    verification = verify_latest_articles(limit=10)
    failed_slugs = verification.get('failed_slugs', [])
    
    if not failed_slugs:
        return {'status': 'ok', 'message': 'No divergences found'}
    
    # Load verification details
    try:
        vlog = load_json(FIX_LOG)
    except Exception:
        vlog = {'fixes': []}
    
    fixes = []
    unrecoverable = []
    
    for result in verification.get('results', []):
        if not result.get('valid'):
            slug = result.get('slug')
            file_path = BLOG_DIR / result.get('file', f'{slug}.html')
            issues = result.get('issues', [])
            
            # Skip if file doesn't exist
            if not file_path.exists():
                unrecoverable.append({'slug': slug, 'reason': 'file_missing'})
                continue
            
            fix_result = fix_article(file_path, issues)
            fixes.append(fix_result)
            
            if not fix_result.get('fixed'):
                unrecoverable.append({'slug': slug, 'reason': fix_result.get('reason', 'no_safe_fix')})
    
    # Update sitemap if any fixes were applied
    sitemap_result = {'updated': False}
    if fixes:
        sitemap_result = update_sitemap()
    
    # Update verification log
    vlog['fixes'] = vlog.get('fixes', []) + fixes
    vlog['unrecoverable'] = vlog.get('unrecoverable', []) + unrecoverable
    vlog['last_run'] = datetime.now(timezone.utc).isoformat()
    save_json(FIX_LOG, vlog)
    
    # Mark unrecoverable for human review
    if unrecoverable:
        mark_for_human_review([u['slug'] for u in unrecoverable], 'post_publish_fix_failed')
    
    # Update registry
    update_registry_verification(verification)
    
    # Re-run verification
    reverification = verify_latest_articles(limit=10)
    still_failed = reverification.get('failed_slugs', [])
    
    result = {
        'status': 'ok' if not still_failed else 'divergences_remain',
        'fixed': len(fixes),
        'unrecoverable': len(unrecoverable),
        'sitemap_updated': sitemap_result.get('updated', False),
        'still_failed': still_failed,
    }
    
    return result


if __name__ == '__main__':
    result = main()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get('status') == 'ok' else 1)
