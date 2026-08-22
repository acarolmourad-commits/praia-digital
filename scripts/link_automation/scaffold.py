"""Scaffold de automação de links — modo dry-run por padrão."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

BASE = Path('C:/Users/Carolina/praia-digital')
SCOPE_ROOTS = [
    BASE / 'blog',
    BASE / 'servicos',
    BASE / 'cidades',
    BASE / 'education',
    BASE / 'anfitrioes',
    BASE / 'assets',
    BASE / 'docs',
]
DO_NOT_TOUCH = [
    BASE / 'academy',
    BASE / 'uploads',
    BASE / 'scripts',
    BASE / 'tests',
    BASE / 'node_modules',
]
LINK_RE = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)
SRC_RE = re.compile(r'src=["\']([^"\']+)["\']', re.IGNORECASE)
DRY_RUN = True
RULE_LOG = BASE / 'scripts/link_automation/rule-log.json'
BATCH_LOG = BASE / 'scripts/link_automation/batch-log.json'


@dataclass
class LinkRule:
    id: str
    pattern: str
    target: str
    evidence: str
    confidence: str
    action: str
    enabled: bool = True


@dataclass
class LinkCandidate:
    source: str
    original_href: str
    target_href: str
    status: str
    link_type: str
    pattern_matched: Optional[str]
    confidence: Optional[str]
    evidence: Optional[str]
    hash_before: str = ''
    hash_after: str = ''


@dataclass
class BatchRecord:
    batch_id: str
    timestamp: str
    dry_run: bool
    candidates: list[LinkCandidate]
    applied: int
    skipped: int
    errors: int


def sha256_file(path: Path) -> str:
    if not path.exists():
        return ''
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_in_scope(html_path: Path) -> bool:
    for forbidden in DO_NOT_TOUCH:
        if str(html_path).startswith(str(forbidden)):
            return False
    for root in SCOPE_ROOTS:
        if str(html_path).startswith(str(root)):
            return True
    return html_path in [BASE / 'index.html', BASE / 'contato.html', BASE / 'servicos.html']


def classify_href(ref: str) -> tuple[str, str]:
    if ref.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', '//', 'data:')):
        return 'EXTERNO' if ref.startswith(('http://', 'https://')) else 'ESPECIAL'
    return 'INTERNO'


def match_rules(ref: str, rules: list[LinkRule]) -> Optional[LinkRule]:
    for rule in rules:
        if not rule.enabled:
            continue
        try:
            if re.search(rule.pattern, ref, re.IGNORECASE):
                return rule
        except re.error:
            continue
    return None


def load_rules() -> list[LinkRule]:
    return [
        LinkRule(
            id='R001',
            pattern=r'^diagnosticos-anfitrioes\.html$',
            target='anfitrioes/diagnosticos-anfitrioes.html',
            evidence='anfitrioes/diagnosticos-anfitrioes.html exists; structured subsite under anfitrioes/',
            confidence='ALTO',
            action='REPARAR',
        ),
        LinkRule(
            id='R002',
            pattern=r'^tutoriais-anfitrioes\.html$',
            target='anfitrioes/tutoriais-anfitrioes.html',
            evidence='anfitrioes/tutoriais-anfitrioes.html exists; structured subsite under anfitrioes/',
            confidence='ALTO',
            action='REPARAR',
        ),
        LinkRule(
            id='R003',
            pattern=r'^checklists-anfitrioes\.html$',
            target='anfitrioes/checklists-anfitrioes.html',
            evidence='anfitrioes/checklists-anfitrioes.html exists; structured subsite under anfitrioes/',
            confidence='ALTO',
            action='REPARAR',
        ),
        LinkRule(
            id='R004',
            pattern=r'^analise-completa-imovel\.html$',
            target='assets/analise-completa-imovel.html',
            evidence='assets/analise-completa-imovel.html exists; asset page exists',
            confidence='ALTO',
            action='REPARAR',
        ),
        LinkRule(
            id='R005',
            pattern=r'^roi-ia-imobiliaria\.html$',
            target='assets/roi-ia-imobiliaria.html',
            evidence='assets/roi-ia-imobiliaria.html exists; asset page exists',
            confidence='ALTO',
            action='REPARAR',
        ),
        LinkRule(
            id='R006',
            pattern=r'^servico-avaliacao-preco-imoveis-litoral\.html$',
            target='assets/servico-avaliacao-preco-imoveis-litoral.html',
            evidence='assets/servico-avaliacao-preco-imoveis-litoral.html exists; asset page exists',
            confidence='ALTO',
            action='REPARAR',
        ),
        LinkRule(
            id='R007',
            pattern=r'^blog/seo-local-imobiliaria-litoral-paulista\.html$',
            target='blog/seo-local-imobiliaria-litoral-paulista-2026.html',
            evidence='blog/seo-local-imobiliaria-litoral-paulista-2026.html exists; slug appears to have been suffixed with year',
            confidence='MEDIO',
            action='REVISÃO_HUMANA',
        ),
        LinkRule(
            id='R008',
            pattern=r'^blog/seo-local-imobiliaria-litoral-paulista-2026\.html$',
            target='blog/seo-local-imobiliaria-litoral-paulista-2026.html',
            evidence='self-link; keep as-is',
            confidence='100%',
            action='VALIDO',
        ),
    ]


def audit_links() -> tuple[list[LinkCandidate], dict[str, int]]:
    rules = load_rules()
    candidates: list[LinkCandidate] = []
    summary: dict[str, int] = {}
    html_files = [p for p in BASE.rglob('*.html') if is_in_scope(p)]
    for html_path in html_files:
        rel = html_path.relative_to(BASE)
        text = html_path.read_text(encoding='utf-8', errors='ignore')
        refs = LINK_RE.findall(text) + SRC_RE.findall(text)
        for ref in refs:
            tipo = classify_href(ref)
            if tipo in ('EXTERNO', 'ESPECIAL'):
                summary[tipo] = summary.get(tipo, 0) + 1
                continue
            target = ref.lstrip('/').replace('/', '\\')
            exists = (BASE / target).exists()
            rule = match_rules(ref, rules)
            if exists:
                status = 'VALIDO'
                conf = '100%'
                evidence = 'target exists'
                matched = None
            elif rule:
                status = rule.action
                conf = rule.confidence
                evidence = rule.evidence
                matched = rule.id
            else:
                status = 'AMBIGUO'
                conf = 'BAIXO'
                evidence = 'no rule matched'
                matched = None
            candidate = LinkCandidate(
                source=str(rel),
                original_href=ref,
                target_href=target,
                status=status,
                link_type=tipo,
                pattern_matched=matched,
                confidence=conf,
                evidence=evidence,
                hash_before=sha256_file(html_path),
            )
            candidates.append(candidate)
            summary[status] = summary.get(status, 0) + 1
    return candidates, summary


def dry_run() -> BatchRecord:
    candidates, summary = audit_links()
    batch_id = datetime.now(timezone.utc).strftime('batch-%Y%m%d-%H%M%S')
    record = BatchRecord(
        batch_id=batch_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        dry_run=True,
        candidates=candidates,
        applied=0,
        skipped=0,
        errors=0,
    )
    out = BASE / 'scripts/link_automation/dry-run-report.json'
    out.write_text(
        json.dumps(
            {
                'batch': asdict(record),
                'summary': summary,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding='utf-8',
    )
    return record


if __name__ == '__main__':
    print('DRY_RUN =', DRY_RUN)
    rec = dry_run()
    print('Candidates:', len(rec.candidates))
    print('Summary:', json.dumps({k: v for k, v in json.loads((BASE / 'scripts/link_automation/dry-run-report.json').read_text(encoding='utf-8'))['summary'].items()}, ensure_ascii=False))
