#!/usr/bin/env python3
"""
Regression test for K3: repeated-word combined bypass.

This test specifically guards the failure mode where K3 was able to pass
the publication gate because check_low_specificity exited early when the
text had fewer than 8 sentences, even though lexical diversity was
extremely low.

A structural fix was applied in publication_gate.py by checking
diversity_ratio before the sentence-count guard, so K3 must now be
blocked with rule=low_specificity and extremely_low_diversity.
"""
import json
import sys
from pathlib import Path

REPO = Path('C:/Users/Carolina/praia-digital')
sys.path.insert(0, str(REPO / 'scripts' / 'orchestrator' / 'modules'))
from publication_gate import validate_article

K3_PATH = REPO / 'docs' / 'seo' / 'tmp_adversarial' / 'K3.html'

def test_k3_is_blocked():
    assert K3_PATH.exists(), f'Missing K3 fixture at {K3_PATH}'
    result = validate_article(K3_PATH)

    print('K3 regression result:')
    print(json.dumps(result, ensure_ascii=False, indent=2))

    assert result['pass'] is False, 'K3 should not pass publication gate'
    assert result['blocked'] is True, 'K3 should be explicitly blocked'

    rules = [issue['rule'] for issue in result['issues']]
    assert 'low_specificity' in rules, f'Expected low_specificity in issues, got {rules}'

    low_spec_issues = [i for i in result['issues'] if i['rule'] == 'low_specificity']
    assert low_spec_issues, 'low_specificity issue should exist'
    detail = low_spec_issues[0].get('found', '')
    assert 'extremely_low_diversity' in detail, f'Expected extremely_low_diversity in detail, got {detail}'

if __name__ == '__main__':
    test_k3_is_blocked()
    print('OK: K3 regression test passed.')
