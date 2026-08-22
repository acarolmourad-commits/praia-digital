#!/usr/bin/env python3
"""
P1-2 SEO/H1/Schema audit gate.

Scans HTML pages and produces:
- PASS
- FAIL
- WARNING

with per-URL evidence for:
TITLE, META, CANONICAL, H1, SCHEMA, STATUS
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


def _first(regex: re.Pattern, text: str) -> str | None:
    match = regex.search(text)
    return match.group(1).strip() if match else None


def _audit_html(text: str) -> dict:
    title = _first(re.compile(r'<title[^>]*>(.*?)</title>', re.S | re.I), text)
    h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', text, re.S | re.I)
    h1_count = len(h1_matches)
    h1 = h1_matches[0].strip() if h1_matches else None
    meta_description = _first(
        re.compile(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', re.I),
        text,
    )
    canonical = _first(
        re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', re.I),
        text,
    )
    if canonical is None:
        canonical = _first(
            re.compile(r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\'][^>]*>', re.I),
            text,
        )
    json_ld_matches = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', text, re.S | re.I)
    schema_valid = True
    schema_errors: list[str] = []
    for block in json_ld_matches:
        try:
            json.loads(block)
        except json.JSONDecodeError as exc:
            schema_valid = False
            schema_errors.append(f"invalid_json: {exc}")
    schema_present = bool(json_ld_matches)

    title_status = AuditStatus.PASS if title else AuditStatus.FAIL
    meta_status = AuditStatus.PASS if meta_description else AuditStatus.FAIL
    h1_status = AuditStatus.PASS if h1_count == 1 else AuditStatus.FAIL if h1_count == 0 else AuditStatus.WARNING
    canonical_status = AuditStatus.PASS if canonical else AuditStatus.WARNING
    schema_status = AuditStatus.PASS if schema_present and schema_valid else AuditStatus.FAIL if not schema_present else AuditStatus.FAIL

    overall = AuditStatus.FAIL if any(status == AuditStatus.FAIL for status in [
        title_status, meta_status, h1_status, canonical_status, schema_status
    ]) else AuditStatus.PASS

    return {
        "title": title,
        "title_status": title_status,
        "meta_description": meta_description,
        "meta_status": meta_status,
        "h1": h1,
        "h1_count": h1_count,
        "h1_status": h1_status,
        "canonical": canonical,
        "canonical_status": canonical_status,
        "schema_present": schema_present,
        "schema_valid": schema_valid,
        "schema_status": schema_status,
        "schema_errors": schema_errors,
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
    warnings = [url for url, data in results.items() if data["overall"] == AuditStatus.WARNING]
    summary = {
        "total": len(results),
        "fail": len(fails),
        "warning": len(warnings),
        "pass": len(results) - len(fails) - len(warnings),
        "examples": {
            "fail": fails[:20],
            "warning": warnings[:20],
        },
    }
    return {"status": AuditStatus.FAIL if fails else AuditStatus.PASS, "summary": summary, "pages": results}


def main() -> int:
    result = audit(limit=200)
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    return 0 if result["status"] == AuditStatus.PASS else 1


if __name__ == "__main__":
    sys.exit(main())
