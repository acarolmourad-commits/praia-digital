from __future__ import annotations

from scripts.automation.image_audit import _audit_html


def _html(images=0, alt=0, width_height=0, lazy=0, large=0):
    parts = ['<!DOCTYPE html><html><body>']
    for i in range(images):
        a = ' alt="img"' if i < alt else ''
        wh = ' width="100" height="100"' if i < width_height else ''
        lz = ' loading="lazy"' if i < lazy else ''
        parts.append(f'<img src="img{i}.webp"{a}{wh}{lz}>')
    parts.append('</body></html>')
    return '\n'.join(parts)


def test_image_audit_counts():
    html = _html(images=5, alt=3, width_height=2, lazy=1, large=0)
    result = _audit_html(html)
    assert result['total'] == 5
    assert result['missing_alt'] == 2
    assert result['missing_width_height'] == 3
    assert result['missing_lazy'] == 4


def test_image_audit_all_good():
    html = _html(images=2, alt=2, width_height=2, lazy=2, large=0)
    result = _audit_html(html)
    assert result['missing_alt'] == 0
    assert result['missing_width_height'] == 0
    assert result['missing_lazy'] == 0
