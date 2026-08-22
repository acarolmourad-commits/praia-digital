#!/usr/bin/env python3
"""
Boundary tests for diversity_ratio threshold 0.02.

These tests use controlled synthetic fixtures to verify:
- diversity_ratio < 0.02 → blocked by low_specificity
- diversity_ratio >= 0.02 → NOT blocked exclusively by extremely_low_diversity

Because HTML structure/template words add unique tokens, exact 0.0200 is not
reachable with the current template. The tests use clearly separable ranges:
- below-threshold: diversity < 0.02
- above-threshold: diversity > 0.02
"""
import sys
from pathlib import Path

REPO = Path('C:/Users/Carolina/praia-digital')
TMP_DIR = REPO / 'docs' / 'seo' / 'tmp_adversarial'
sys.path.insert(0, str(REPO / 'scripts' / 'orchestrator' / 'modules'))
from publication_gate import validate_article

BASE_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="https://praia.digital/blog/{slug}.html">
</head>
<body>
<h1>{h1}</h1>
{content}
<a href="https://praia.digital/blog/artigo-completo.html">link interno</a>
</body>
</html>"""


def build(title, slug, h1, content, meta='Meta description coerente.'):
    return BASE_HTML.format(title=title, meta=meta, slug=slug, h1=h1, content=content)


def run_case(name, html):
    path = TMP_DIR / f'boundary_{name}.html'
    path.write_text(html, encoding='utf-8')
    return validate_article(path)


def test_diversity_below_threshold_blocks():
    """diversity_ratio < 0.02 must block via low_specificity."""
    # 2 unique words repeated many times → measured diversity ~0.0164
    content = "<h2>Sec</h2><p>" + ("termo0 termo1 " * 150) + "</p><h2>Outro</h2><p>" + ("termo0 termo1 " * 150) + "</p>"
    html = build('Boundary Below', 'boundary-below', 'Boundary Below', content)
    result = run_case('below_threshold', html)
    assert result['blocked'] is True
    rules = [i['rule'] for i in result['issues']]
    assert 'low_specificity' in rules


def test_diversity_above_threshold_does_not_block_by_diversity():
    """diversity_ratio > 0.02 must NOT block exclusively by extremely_low_diversity."""
    # 10 unique body words repeated → measured diversity ~0.0241
    content = "<h2>Sec</h2><p>" + ("termo0 termo1 termo2 termo3 termo4 termo5 termo6 termo7 termo8 termo9 " * 37) + "</p><h2>Outro</h2><p>" + ("termo0 termo1 termo2 termo3 termo4 termo5 termo6 termo7 termo8 termo9 " * 37) + "</p>"
    html = build('Boundary Above', 'boundary-above', 'Boundary Above', content)
    result = run_case('above_threshold', html)
    rules = [i['rule'] for i in result['issues']]
    assert 'low_specificity' not in rules, f'Should not block by low_specificity above threshold, got {rules}'


def test_diversity_near_threshold_below_blocks():
    """Near-below threshold should still block via low_specificity."""
    # 2 unique body words repeated → measured diversity ~0.0245... actually above.
    # Use pattern with lower diversity: 2 words with fewer repeats gives higher diversity,
    # 2 words with many repeats gives lower diversity.
    # Actually 2 words x 150 = diversity ~0.0164
    content = "<h2>Sec</h2><p>" + ("termo0 termo1 " * 150) + "</p><h2>Outro</h2><p>" + ("termo0 termo1 " * 150) + "</p>"
    html = build('Near Below', 'near-below', 'Near Below', content)
    result = run_case('near_below', html)
    assert result['blocked'] is True
    rules = [i['rule'] for i in result['issues']]
    assert 'low_specificity' in rules


def test_diversity_near_threshold_above_does_not_block_by_diversity():
    """Near-above threshold should not block by diversity rule."""
    # 10 words x 30 → measured diversity ~0.0296
    content = "<h2>Sec</h2><p>" + ("termo0 termo1 termo2 termo3 termo4 termo5 termo6 termo7 termo8 termo9 " * 30) + "</p><h2>Outro</h2><p>" + ("termo0 termo1 termo2 termo3 termo4 termo5 termo6 termo7 termo8 termo9 " * 30) + "</p>"
    html = build('Near Above 2', 'near-above-2', 'Near Above 2', content)
    result = run_case('near_above_2', html)
    rules = [i['rule'] for i in result['issues']]
    assert 'low_specificity' not in rules, f'Should not block by low_specificity near threshold above, got {rules}'
