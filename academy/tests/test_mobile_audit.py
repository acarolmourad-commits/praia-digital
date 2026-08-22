from __future__ import annotations

from scripts.mobile.mobile_audit import _audit_html


def _html(viewport=True, whatsapp=True, inputs=0, images=0, fixed_width=False):
    parts = ["<!DOCTYPE html><html lang=\"pt-BR\"><head>"]
    if viewport:
        parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    if whatsapp:
        parts.append('<a href="https://wa.me/123">WhatsApp</a>')
    parts.append("</head><body>")
    for _ in range(inputs):
        parts.append('<input type="text" aria-label="Nome">')
    for _ in range(images):
        parts.append('<img src="x.jpg" width="100%">')
    if fixed_width:
        parts.append('<div style="width:1000px">X</div>')
    parts.append("</body></html>")
    return "\n".join(parts)


def test_pass_when_ok():
    html = _html(viewport=True, whatsapp=True, inputs=1, images=1, fixed_width=False)
    result = _audit_html(html)
    assert result["overall"] == "PASS"


def test_fail_without_viewport():
    html = _html(viewport=False, whatsapp=True)
    result = _audit_html(html)
    assert result["overall"] == "FAIL"
    assert "missing_viewport" in result["issues"]


def test_fail_without_whatsapp():
    html = _html(viewport=True, whatsapp=False)
    result = _audit_html(html)
    assert result["overall"] == "FAIL"
    assert "missing_whatsapp_cta" in result["issues"]


def test_fixed_width_detected():
    html = '<html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head><body><a href="https://wa.me/123">W</a><div style="width:1000px">X</div></body></html>'
    result = _audit_html(html)
    assert "fixed_width_detected" in result["issues"]
    assert result["overall"] == "PASS"


def test_non_responsive_images_detected():
    html = '<html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head><body><a href="https://wa.me/123">W</a><img src="x.jpg" width="300px"></body></html>'
    result = _audit_html(html)
    assert result["non_responsive_images"] == 1
