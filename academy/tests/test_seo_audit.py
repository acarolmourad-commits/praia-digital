from __future__ import annotations

import json

from scripts.seo.seo_audit import _audit_html


def _html(title=None, meta=None, h1=None, h1_count=1, canonical=None, schema_present=True, schema_valid=True, noindex=False):
    parts = ["<!DOCTYPE html><html lang=\"pt-BR\"><head>"]
    if title:
        parts.append(f"<title>{title}</title>")
    if meta:
        parts.append(f'<meta name="description" content="{meta}">')
    if canonical:
        parts.append(f'<link rel="canonical" href="{canonical}">')
    if schema_present:
        block = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": "ok"})
        parts.append(f'<script type="application/ld+json">{block}</script>')
    if noindex:
        parts.append('<meta name="robots" content="noindex">')
    parts.append("</head><body>")
    if h1_count >= 1:
        parts.append(f"<h1>{h1 or 'H1'}</h1>")
    for _ in range(max(0, h1_count - 1)):
        parts.append("<h1>Extra</h1>")
    parts.append("</body></html>")
    return "\n".join(parts)


def test_valid_page():
    html = _html(title="T", meta="M" * 60, canonical="https://example.com/x", h1="H1")
    result = _audit_html(html)
    assert result["overall"] == "PASS"
    assert result["title_status"] == "PASS"
    assert result["meta_status"] == "PASS"
    assert result["h1_status"] == "PASS"
    assert result["canonical_status"] == "PASS"
    assert result["schema_status"] == "PASS"


def test_missing_title_fails():
    html = _html(meta="M" * 60, canonical="https://example.com/x", h1="H1")
    result = _audit_html(html)
    assert result["title_status"] == "FAIL"
    assert result["overall"] == "FAIL"


def test_missing_meta_fails():
    html = _html(title="T", canonical="https://example.com/x", h1="H1")
    result = _audit_html(html)
    assert result["meta_status"] == "FAIL"
    assert result["overall"] == "FAIL"


def test_missing_h1_fails():
    html = _html(title="T", meta="M" * 60, canonical="https://example.com/x", h1_count=0)
    result = _audit_html(html)
    assert result["h1_status"] == "FAIL"
    assert result["overall"] == "FAIL"


def test_multiple_h1_is_warning():
    html = _html(title="T", meta="M" * 60, canonical="https://example.com/x", h1_count=2)
    result = _audit_html(html)
    assert result["h1_status"] == "WARNING"
    assert result["overall"] == "PASS"


def test_missing_canonical_is_warning():
    html = _html(title="T", meta="M" * 60, h1="H1")
    result = _audit_html(html)
    assert result["canonical_status"] == "WARNING"
    assert result["overall"] == "PASS"


def test_invalid_schema_fails():
    html = _html(title="T", meta="M" * 60, canonical="https://example.com/x", h1="H1")
    bad = '<script type="application/ld+json">{invalid json}</script>'
    html = html.replace("</head>", bad + "</head>")
    result = _audit_html(html)
    assert result["schema_status"] == "FAIL"
    assert result["schema_valid"] is False
    assert result["overall"] == "FAIL"


def test_long_content_page():
    html = _html(title="T", meta="M" * 60, canonical="https://example.com/x", h1="H1")
    html = html.replace("</body>", "<article>" + "x" * 5000 + "</article></body>")
    result = _audit_html(html)
    assert result["overall"] == "PASS"
