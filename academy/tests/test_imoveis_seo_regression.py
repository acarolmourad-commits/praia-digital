from __future__ import annotations

from pathlib import Path

from scripts.seo.seo_audit import _audit_html


IMOVEIS_DIR = Path(__file__).resolve().parent.parent.parent / 'imoveis'


def _read_sample(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='ignore')


def test_imoveis_pages_have_h1():
    missing = []
    for path in sorted(IMOVEIS_DIR.glob('*.html')):
        html = _read_sample(path)
        result = _audit_html(html)
        if result['h1_status'] != 'PASS':
            missing.append(path.name)
    assert not missing, f'{len(missing)} imoveis pages missing H1: {missing[:5]}'


def test_imoveis_pages_pass_seo_audit():
    fails = []
    for path in sorted(IMOVEIS_DIR.glob('*.html')):
        html = _read_sample(path)
        result = _audit_html(html)
        if result['overall'] != 'PASS':
            fails.append((path.name, result['overall']))
    assert not fails, f'{len(fails)} imoveis pages failing SEO audit: {fails[:5]}'
