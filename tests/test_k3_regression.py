#!/usr/bin/env python3
"""
K3 regression and sentence-count bypass protection.

These tests guarantee that:
1. K3 remains blocked by low_specificity due to extremely low diversity.
2. Content with sentence_count < 8 and very low diversity is still blocked
   before the sentence-count guard can bypass diversity evaluation.
"""
import json
import sys
from pathlib import Path

REPO = Path('C:/Users/Carolina/praia-digital')
sys.path.insert(0, str(REPO / 'scripts' / 'orchestrator' / 'modules'))
from publication_gate import validate_article

TMP_DIR = REPO / 'docs' / 'seo' / 'tmp_adversarial'
K3_PATH = TMP_DIR / 'K3.html'


def test_k3_remains_blocked():
    assert K3_PATH.exists(), f'Missing K3 fixture at {K3_PATH}'
    result = validate_article(K3_PATH)
    assert result['blocked'] is True
    rules = [i['rule'] for i in result['issues']]
    assert 'low_specificity' in rules
    detail = next(i['found'] for i in result['issues'] if i['rule'] == 'low_specificity')
    assert 'extremely_low_diversity' in detail


def test_low_diversity_with_few_sentences_blocks():
    """Protect against the original K3 bypass path:
    sentence_count < 8 should not prevent diversity evaluation."""
    # 7 sentences, very low diversity, all other gates satisfied
    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Bypass Protection</title>
<meta name="description" content="Meta description coerente e válida.">
<link rel="canonical" href="https://praia.digital/blog/bypass-protection.html">
</head>
<body>
<h1>Bypass Protection</h1>
<h2>Sec</h2>
<p>{content}</p>
<h2>Outro</h2>
<p>{content2}</p>
<a href="https://praia.digital/blog/artigo-completo.html">link interno</a>
</body>
</html>"""
    # Use 2 unique words repeated many times → diversity ~0.02 boundary
    content = 'palavra_a palavra_b ' * 120
    html = html.format(content=content, content2=content)
    path = TMP_DIR / 'sentence_bypass_protection.html'
    path.write_text(html, encoding='utf-8')
    result = validate_article(path)
    assert result['blocked'] is True
    rules = [i['rule'] for i in result['issues']]
    assert 'low_specificity' in rules
