#!/usr/bin/env python3
"""
Duplicate content manager for Praia Digital.
Identifies duplicate signals and applies canonical consolidation
without removing pages automatically.
"""
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

REPO = Path(__file__).resolve().parents[3]
BLOG_DIR = REPO / 'blog'
BANK_PATH = REPO / 'docs' / 'banco-editorial.json'
CANONICAL_REPORT_PATH = REPO / 'docs' / 'canonical_consolidation_report.json'

MIN_DUPLICATE_SCORE = 0.9


def load_bank():
    if not BANK_PATH.exists():
        raise FileNotFoundError(f'Banco editorial não encontrado: {BANK_PATH}')
    return json.loads(BANK_PATH.read_text(encoding='utf-8'))


def get_duplicate_signals(data, min_score=MIN_DUPLICATE_SCORE):
    """Get duplicate signals above threshold."""
    signals = data.get('duplicate_signals', [])
    return [s for s in signals if s.get('score', 0) >= min_score]


def resolve_path(slug_or_path):
    """Resolve article path from slug or relative path."""
    normalized = slug_or_path.replace('\\', '/')
    p = Path(normalized)
    if p.suffix:
        return p
    return p.with_suffix('.html')


def read_article_html(path: Path):
    """Read article HTML."""
    if not path.exists():
        return None
    return path.read_text(encoding='utf-8', errors='ignore')


def extract_canonical(html: str):
    """Extract existing canonical URL."""
    m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', html, re.I)
    return m.group(1) if m else None


def upsert_canonical(html: str, canonical_url: str):
    """Add or replace canonical link."""
    if re.search(r'<link[^>]+rel=["\']canonical["\']', html, re.I):
        return re.sub(
            r'<link[^>]+rel=["\']canonical["\'][^>]+>',
            f'<link rel="canonical" href="{canonical_url}"/>',
            html,
            count=1,
            flags=re.I
        )
    # Insert before </head>
    html = html.replace('</head>', f'<link rel="canonical" href="{canonical_url}"/>\n</head>', 1)
    return html


def consolidate_duplicates(signals):
    """
    For each duplicate pair, designate the first occurrence as canonical
    and add canonical link to the second occurrence.
    Returns report of changes.
    """
    data = load_bank()
    articles = data.get('articles', [])
    
    # Build slug -> article mapping
    slug_map = {}
    for a in articles:
        title = a.get('title') or a.get('titulo') or ''
        city = a.get('city') or ''
        path = a.get('path', '')
        if path:
            slug = Path(path).stem
            slug_map[slug] = a
    
    report = []
    changed = []
    
    for signal in signals:
        a_path = signal.get('a', '')
        b_path = signal.get('b', '')
        
        a_full = REPO / resolve_path(a_path)
        b_full = REPO / resolve_path(b_path)
        
        a_html = read_article_html(a_full)
        b_html = read_article_html(b_full)
        
        if not a_html or not b_html:
            continue
        
        # Determine canonical: keep the one with longer content or earlier date
        a_len = len(a_html)
        b_len = len(b_html)
        
        if a_len >= b_len:
            canonical_path = a_full
            duplicate_path = b_full
            canonical_slug = a_full.stem
            duplicate_slug = b_full.stem
        else:
            canonical_path = b_full
            duplicate_path = a_full
            canonical_slug = b_full.stem
            duplicate_slug = a_full.stem
        
        canonical_url = f'https://praia.digital/blog/{canonical_slug}.html'
        
        # Update canonical link on duplicate page
        updated_html = upsert_canonical(b_html, canonical_url)
        
        if updated_html != b_html:
            duplicate_path.write_text(updated_html, encoding='utf-8')
            changed.append({
                'duplicate': str(duplicate_path.relative_to(REPO)),
                'canonical': str(canonical_path.relative_to(REPO)),
                'canonical_url': canonical_url,
                'score': signal.get('score'),
                'reason': signal.get('reason'),
            })
        
        report.append({
            'pair': [str(a_full.relative_to(REPO)), str(b_full.relative_to(REPO))],
            'canonical': str(canonical_path.relative_to(REPO)),
            'duplicate': str(duplicate_path.relative_to(REPO)),
            'score': signal.get('score'),
            'reason': signal.get('reason'),
            'action': 'canonicalized' if updated_html != b_html else 'unchanged',
        })
    
    return report, changed


def generate_report(report, changed):
    """Save consolidation report."""
    output = {
        'generated_at': datetime.now().isoformat(),
        'total_signals': len(report),
        'changed': len(changed),
        'unchanged': len(report) - len(changed),
        'report': report,
        'changed_entries': changed,
    }
    
    CANONICAL_REPORT_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    return output


def main():
    data = load_bank()
    signals = get_duplicate_signals(data)
    
    print(f'=== DUPLICATE CONTENT AUDIT ===')
    print(f'Total duplicate signals: {len(signals)}')
    
    if not signals:
        print('No duplicates above threshold.')
        return
    
    report, changed = consolidate_duplicates(signals)
    result = generate_report(report, changed)
    
    print(f'Processed: {result["total_signals"]}')
    print(f'Canonicalized: {result["changed"]}')
    print(f'Unchanged: {result["unchanged"]}')
    print(f'\nReport saved to: {CANONICAL_REPORT_PATH}')
    
    if changed:
        print('\nTop changed entries:')
        for entry in changed[:5]:
            print(f"  {entry['duplicate']} -> {entry['canonical']} (score={entry['score']})")


if __name__ == '__main__':
    main()
