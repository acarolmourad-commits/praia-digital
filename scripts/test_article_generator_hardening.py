#!/usr/bin/env python3
"""
Hardening tests for article_generator.py fail-closed behavior.

Validates that when the Publication Gate is unavailable for any reason,
publication is blocked rather than silently skipped.
"""
import sys
import types
from pathlib import Path

REPO = Path('C:/Users/Carolina/praia-digital')
TMP = REPO / 'docs' / 'seo' / 'tmp_adversarial'
sys.path.insert(0, str(REPO / 'scripts' / 'orchestrator' / 'modules'))
from article_generator import (
    load_publication_gate,
    validate_generated_article,
    PublicationGateError,
    PUBLICATION_GATE,
)

# Use a known-passing real blog article for valid-content tests
VALID_HTML_PATH = REPO / 'blog' / '3-erros-que-matam-vendas-de-temporada-no-litoral-lote-2026-08-03-23.html'
VALID_HTML = VALID_HTML_PATH.read_text(encoding='utf-8', errors='ignore')


def test_gate_available_valid_content():
    """T5: Gate available, valid content → normal validation flow (PASS)."""
    path = TMP / 'HARDEN_T5.html'
    path.write_text(VALID_HTML, encoding='utf-8')
    try:
        validate_generated_article(VALID_HTML, path)
        print('T5: PASS (no exception)')
    except PublicationGateError as e:
        print(f'T5: FAIL -> {e}')
        raise AssertionError('T5 should pass with valid content and available gate')


def test_gate_unavailable_content_valid():
    """T1: Content valid, gate unavailable → MUST BLOCK."""
    import article_generator
    original_path = article_generator.PUBLICATION_GATE
    try:
        article_generator.PUBLICATION_GATE = REPO / 'nonexistent' / 'publication_gate.py'
        path = TMP / 'HARDEN_T1.html'
        path.write_text(VALID_HTML, encoding='utf-8')
        try:
            validate_generated_article(VALID_HTML, path)
            raise AssertionError('T1: FAIL - publication was not blocked when gate was unavailable')
        except PublicationGateError as e:
            issues = e.issues if hasattr(e, 'issues') else []
            rules = [i.get('rule') for i in issues]
            assert 'publication_gate_unavailable' in rules, f'T1: Expected publication_gate_unavailable, got {rules}'
            print(f'T1: BLOCK as expected -> rule={rules}')
    finally:
        article_generator.PUBLICATION_GATE = original_path


def test_import_error_fail_closed():
    """T2: Simulate ImportError during gate loading → MUST BLOCK."""
    import article_generator
    original_fn = article_generator.load_publication_gate

    def mock_load():
        raise ImportError('Simulated import failure')

    article_generator.load_publication_gate = mock_load
    try:
        path = TMP / 'HARDEN_T2.html'
        path.write_text(VALID_HTML, encoding='utf-8')
        try:
            validate_generated_article(VALID_HTML, path)
            raise AssertionError('T2: FAIL - publication was not blocked on ImportError')
        except PublicationGateError as e:
            issues = e.issues if hasattr(e, 'issues') else []
            rules = [i.get('rule') for i in issues]
            assert 'publication_gate_unavailable' in rules, f'T2: Expected publication_gate_unavailable, got {rules}'
            print(f'T2: BLOCK as expected -> rule={rules}')
    finally:
        article_generator.load_publication_gate = original_fn


def test_invalid_api_fail_closed():
    """T3: Module loads but missing expected API → MUST BLOCK."""
    import article_generator
    original_fn = article_generator.load_publication_gate

    def mock_load():
        m = types.SimpleNamespace()
        m.something_else = True
        return m

    article_generator.load_publication_gate = mock_load
    try:
        path = TMP / 'HARDEN_T3.html'
        path.write_text(VALID_HTML, encoding='utf-8')
        try:
            validate_generated_article(VALID_HTML, path)
            raise AssertionError('T3: FAIL - publication was not blocked with invalid API')
        except PublicationGateError as e:
            issues = e.issues if hasattr(e, 'issues') else []
            rules = [i.get('rule') for i in issues]
            assert 'publication_gate_unavailable' in rules, f'T3: Expected publication_gate_unavailable, got {rules}'
            print(f'T3: BLOCK as expected -> rule={rules}')
    finally:
        article_generator.load_publication_gate = original_fn


def test_exception_during_load_fail_closed():
    """T4: Exception during module execution → MUST BLOCK."""
    import article_generator
    original_fn = article_generator.load_publication_gate

    def mock_load():
        raise RuntimeError('Simulated execution failure')

    article_generator.load_publication_gate = mock_load
    try:
        path = TMP / 'HARDEN_T4.html'
        path.write_text(VALID_HTML, encoding='utf-8')
        try:
            validate_generated_article(VALID_HTML, path)
            raise AssertionError('T4: FAIL - publication was not blocked on exception')
        except PublicationGateError as e:
            issues = e.issues if hasattr(e, 'issues') else []
            rules = [i.get('rule') for i in issues]
            assert 'publication_gate_unavailable' in rules, f'T4: Expected publication_gate_unavailable, got {rules}'
            print(f'T4: BLOCK as expected -> rule={rules}')
    finally:
        article_generator.load_publication_gate = original_fn


if __name__ == '__main__':
    test_gate_available_valid_content()
    test_gate_unavailable_content_valid()
    test_import_error_fail_closed()
    test_invalid_api_fail_closed()
    test_exception_during_load_fail_closed()
    print('\nAll hardening tests passed.')
