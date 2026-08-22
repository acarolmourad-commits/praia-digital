#!/usr/bin/env python3
"""
P2-9 lightweight image audit.
Reports:
- total images
- missing alt
- missing width/height
- non-webp formats
- large images (>200KB)
- lazy loading missing
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

IMAGE_PATTERNS = [
    r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>',
    r'<source[^>]+srcset=["\']([^"\']+)["\'][^>]*>',
]

LARGE_THRESHOLD = 200 * 1024


def _audit_html(text: str) -> dict:
    stats = {
        'total': 0,
        'missing_alt': 0,
        'missing_width_height': 0,
        'non_webp': 0,
        'large': 0,
        'missing_lazy': 0,
    }
    for pat in IMAGE_PATTERNS:
        for m in re.finditer(pat, text, re.I):
            stats['total'] += 1
            tag = m.group(0)
            if 'alt=' not in tag.lower():
                stats['missing_alt'] += 1
            if 'width=' not in tag.lower() or 'height=' not in tag.lower():
                stats['missing_width_height'] += 1
            src = m.group(1)
            if src.lower().endswith('.webp') or '.webp?' in src.lower():
                pass
            elif src.startswith('http'):
                stats['non_webp'] += 1
            else:
                local = REPO / src
                if local.exists() and local.stat().st_size > LARGE_THRESHOLD:
                    stats['large'] += 1
            if 'loading=' not in tag.lower() and not tag.lower().startswith('<source'):
                stats['missing_lazy'] += 1
    return stats


if __name__ == '__main__':
    stats = _audit_html('')
    for path in REPO.glob('**/*.html'):
        rel = str(path.relative_to(REPO)).replace('\\', '/')
        if any(p in rel for p in ['/node_modules/', '/.git/', '/backups/', '/dashboards/', '/api/', '/backend/', '/automation/', 'litoral-prime-imoveis/automation']):
            continue
        txt = path.read_text(encoding='utf-8', errors='ignore')
        result = _audit_html(txt)
        for k, v in result.items():
            stats[k] += v
    print('IMAGE AUDIT:')
    for k, v in stats.items():
        print(f'  {k}: {v}')
