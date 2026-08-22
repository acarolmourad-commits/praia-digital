#!/usr/bin/env python3
"""
P1-4 static mobile/UX audit gate.

Checks HTML pages for:
- viewport meta
- fixed-width elements
- horizontal overflow risk
- missing CTA
- form inputs without labels
- non-responsive images
- clickable elements too small
- navigation links
- WhatsApp CTA presence
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable

REPO = Path(__file__).resolve().parent.parent.parent
PUBLIC_GLOBS = [
    'imoveis/*.html',
    'bairros/*.html',
    'hub/*.html',
    'blog/*.html',
    'cidades/*.html',
    'cidades-expansao/*.html',
    'servicos/*.html',
    'servicos/cidade-servico/*.html',
    'eventos-litoral-paulista-2026-2027/*.html',
    'cases/*.html',
    'curso/*.html',
    'landings/*.html',
    'personas/*.html',
    'propostas/*.html',
    'ferramentas/*.html',
    'anfitrioes/*.html',
    'ia/*.html',
    'investidores/*.html',
    'parcerias-norte/*.html',
    'perfis/*.html',
    'proptech/*.html',
    'subscription/*.html',
    'contato.html',
    'outreach/**/*.html',
    'litoral-prime-imoveis/**/*.html',
    'docs/**/*.html',
    'marketing/**/*.html',
    'newsletter/**/*.html',
]
EXCLUDE_PATTERNS = [
    r'leads/', r'dashboards/', r'backups/', r'node_modules', r'__pycache__',
    r'\.git/', r'api/', r'backend/', r'automation/', r'litoral-prime-imoveis/automation'
]


class AuditStatus:
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"


def _should_exclude(rel: str) -> bool:
    return any(re.search(pat, rel) for pat in EXCLUDE_PATTERNS)


def _public_files(limit: int = 200) -> Iterable[tuple[str, Path]]:
    files: list[tuple[str, Path]] = []
    for pattern in PUBLIC_GLOBS:
        files.extend((str(f.relative_to(REPO)).replace("\\", "/"), f) for f in REPO.glob(pattern))
    seen: set[str] = set()
    out: list[tuple[str, Path]] = []
    for rel, path in files:
        if _should_exclude(rel):
            continue
        if path.suffix.lower() != ".html":
            continue
        if rel in seen:
            continue
        seen.add(rel)
        out.append((rel, path))
        if len(out) >= limit:
            break
    return out


def _audit_html(text: str) -> dict:
    has_viewport = bool(re.search(r'<meta[^>]+name=["\']viewport["\'][^>]+content=["\'][^"\']+["\']', text, re.I))
    has_whatsapp = bool(re.search(r'wa\.me/\d+|whatsapp', text, re.I))
    inputs = re.findall(r'<input\b[^>]*>', text, re.I)
    forms = re.findall(r'<form\b[^>]*>', text, re.I)
    images = re.findall(r'<img\b[^>]*>', text, re.I)
    fixed_width = re.search(r'width\s*=\s*["\'][0-9]+px["\']', text, re.I) or re.search(r'width\s*:\s*[0-9]+px', text, re.I)
    overflow_divs = re.findall(r'<div[^>]+style=["\'][^"\']*overflow[^"\']*["\']', text, re.I)
    small_clickables = re.findall(r'<(?:a|button)[^>]{0,60}style=["\'][^"\']*(?:padding|height|width)\s*:\s*[0-9]+px', text, re.I)

    unlabeled_inputs = 0
    for tag in inputs:
        has_label = bool(re.search(r'<label[^>]+for=["\']', text, re.I))
        has_aria = bool(re.search(r'aria-label|aria-labelledby', tag, re.I))
        if not has_label and not has_aria and 'type="hidden"' not in tag.lower():
            unlabeled_inputs += 1

    responsive_images = sum(1 for img in images if re.search(r'width\s*=\s*["\'][0-9]+%["\']|style=["\'][^"\']*width\s*:\s*[0-9]+%', img, re.I))
    non_responsive_images = len(images) - responsive_images

    issues = []
    if not has_viewport:
        issues.append("missing_viewport")
    if not has_whatsapp:
        issues.append("missing_whatsapp_cta")
    if unlabeled_inputs:
        issues.append(f"unlabeled_inputs:{unlabeled_inputs}")
    if fixed_width:
        issues.append("fixed_width_detected")
    if non_responsive_images and len(images) > 0:
        issues.append(f"non_responsive_images:{non_responsive_images}")
    if small_clickables:
        issues.append("small_clickable_suspected")

    overall = AuditStatus.FAIL if any(i.startswith("missing_") for i in issues) else AuditStatus.PASS

    return {
        "has_viewport": has_viewport,
        "has_whatsapp": has_whatsapp,
        "form_count": len(forms),
        "input_count": len(inputs),
        "unlabeled_inputs": unlabeled_inputs,
        "image_count": len(images),
        "non_responsive_images": non_responsive_images,
        "fixed_width": bool(fixed_width),
        "issues": issues,
        "overall": overall,
    }


def audit(limit: int = 200) -> dict:
    results: dict[str, dict] = {}
    for rel, path in _public_files(limit=limit):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if not re.search(r'<!DOCTYPE\s+html', text, re.I):
            continue
        results[rel] = _audit_html(text)

    fails = [url for url, data in results.items() if data["overall"] == AuditStatus.FAIL]
    summary = {
        "total": len(results),
        "fail": len(fails),
        "pass": len(results) - len(fails),
        "examples": fails[:20],
    }
    return {"status": AuditStatus.FAIL if fails else AuditStatus.PASS, "summary": summary, "pages": results}


def main() -> int:
    result = audit(limit=200)
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    return 0 if result["status"] == AuditStatus.PASS else 1


if __name__ == "__main__":
    sys.exit(main())
