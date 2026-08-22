"""Classify duplicate groups and create consolidation backlog."""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital')
REPORT = BASE / 'scripts/dup_audit_report.json'
CLASSIFICATION = BASE / 'scripts/dup_classification_report.json'
BACKLOG = BASE / 'scripts/dup_consolidation_backlog.json'

TITLE_RE = re.compile(r'<title[^>]*>(.*?)</title>', re.I | re.S)
H1_RE = re.compile(r'<h1[^>]*>(.*?)</h1>', re.I | re.S)
BODY_RE = re.compile(r'<body[^>]*>(.*?)</body>', re.I | re.S)


def clean(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip() if text else ''


def content_hash(text: str) -> str:
    body = BODY_RE.search(text)
    content = body.group(1) if body else text
    normalized = re.sub(r'\s+', ' ', content).strip().lower()
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()[:16]


def classify_group(files):
    if len(files) < 2:
        return 'AMBIGUO'

    contents = []
    hashes = []
    titles = []
    h1s = []
    for f in files[:5]:
        try:
            text = (BASE / f).read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        contents.append(text)
        hashes.append(content_hash(text))
        m = TITLE_RE.search(text)
        titles.append(clean(m.group(1)) if m else '')
        m = H1_RE.search(text)
        h1s.append(clean(m.group(1)) if m else '')

    if not contents:
        return 'AMBIGUO'

    # Check for exact duplicates
    if len(set(hashes)) == 1:
        return 'DUPLICATA_EXATA'

    # Check for same title/h1
    same_title = len(set(titles)) == 1 and titles[0]
    same_h1 = len(set(h1s)) == 1 and h1s[0]

    if same_title and same_h1:
        # Same identity, different content
        return 'SOBREPOSICAO_PARCIAL'

    if same_title or same_h1:
        # Similar identity
        return 'DUPLICATA_FUNCIONAL'

    # Check if URLs indicate different purposes
    urls = [f.lower() for f in files]
    if any('cidade' in u or 'bairro' in u for u in urls):
        if any('servico' in u for u in urls):
            return 'SEMELHANCA_NECESSARIA'

    if any('/blog/' in u for u in urls):
        return 'SEMELHANCA_NECESSARIA'

    return 'AMBIGUO'


def auto_consolidate(classification):
    return classification in ['DUPLICATA_EXATA']


def main():
    report = json.loads(REPORT.read_text(encoding='utf-8'))
    groups = report['details']

    classifications = {
        'DUPLICATA_EXATA': 0,
        'DUPLICATA_FUNCIONAL': 0,
        'SOBREPOSICAO_PARCIAL': 0,
        'SEMELHANCA_NECESSARIA': 0,
        'AMBIGUO': 0,
    }

    auto_candidates = []
    human_review = []

    for g in groups:
        cls = classify_group(g['files'])
        classifications[cls] += 1

        entry = {
            'title': g['title'],
            'h1': g['h1'],
            'files': g['files'],
            'classification': cls,
            'auto_consolidate': auto_consolidate(cls),
            'human_review': not auto_consolidate(cls),
            'action': 'CONSOLIDAR_AUTOMATICAMENTE' if auto_consolidate(cls) else 'REVISAR_MANUAL',
        }

        if auto_consolidate(cls):
            auto_candidates.append(entry)
        else:
            human_review.append(entry)

    output = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'total_groups': len(groups),
        'classifications': classifications,
        'auto_candidates': len(auto_candidates),
        'human_review': len(human_review),
        'auto_details': auto_candidates[:200],
        'human_details': human_review[:500],
    }

    CLASSIFICATION.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')

    # Create consolidation backlog
    backlog = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'total_candidates': len(auto_candidates),
        'candidates': auto_candidates,
        'rules': [
            {
                'rule': 'R_DUP_EXATA',
                'condition': 'Same title, same H1, same content hash',
                'action': 'CONSOLIDAR_AUTOMATICAMENTE',
                'confidence': '100%',
            }
        ],
    }
    BACKLOG.write_text(json.dumps(backlog, ensure_ascii=False, indent=2), encoding='utf-8')

    print('classification', classifications)
    print('auto_candidates', len(auto_candidates))
    print('human_review', len(human_review))


if __name__ == '__main__':
    main()
