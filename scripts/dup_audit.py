"""Auditoria incremental de duplicidades: title/h1 com checkpoint."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital')
CHECKPOINT = BASE / 'scripts/dup_audit_checkpoint.json'
REPORT = BASE / 'scripts/dup_audit_report.json'
CHUNK = 2000

TITLE_RE = re.compile(r'<title[^>]*>(.*?)</title>', re.I | re.S)
H1_RE = re.compile(r'<h1[^>]*>(.*?)</h1>', re.I | re.S)


def clean(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip() if text else ''


def process_chunk(files):
    pairs = {}
    for path in files:
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        path = path.resolve()
        title = clean(TITLE_RE.search(text).group(1)) if TITLE_RE.search(text) else ''
        h1 = clean(H1_RE.search(text).group(1)) if H1_RE.search(text) else ''
        if title or h1:
            key = f'{title}|||{h1}'
            pairs.setdefault(key, []).append(str(path.relative_to(BASE)))
    return pairs


def load_checkpoint():
    if CHECKPOINT.exists():
        return json.loads(CHECKPOINT.read_text(encoding='utf-8'))
    return {'processed': [], 'pairs': {}}


def save_checkpoint(state):
    CHECKPOINT.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')


def main():
    state = load_checkpoint()
    processed = set(state['processed'])
    pairs = dict(state.get('pairs', {}) or {})

    all_html = sorted([
        p for p in BASE.rglob('*.html')
        if 'academy' not in [part.lower() for part in p.parts]
        and 'uploads' not in [part.lower() for part in p.parts]
    ])
    todo = [p for p in all_html if str(p) not in processed]
    print('remaining', len(todo), 'processed', len(processed))

    done = 0
    while done < len(todo):
        chunk = todo[done:done + CHUNK]
        result = process_chunk(chunk)
        for k, v in result.items():
            pairs.setdefault(k, [])
            pairs[k].extend(x for x in v if x not in pairs[k])
        for p in chunk:
            processed.add(str(p))
        done += len(chunk)
        state = {'processed': sorted(processed), 'pairs': pairs}
        save_checkpoint(state)
        print('progress', done, '/', len(todo), 'pairs', len(pairs))

    dups = {k: v for k, v in pairs.items() if len(v) > 1}
    details = []
    for k in sorted(dups.keys(), key=lambda k: -len(dups[k]))[:1000]:
        parts = k.split('|||', 1) + [''] if '|||' in k else ['', k]
        details.append({'title': parts[0], 'h1': parts[1], 'files': dups[k]})
    report = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'total_files': len(all_html),
        'indexed': len(pairs),
        'duplicates': len(dups),
        'details': details,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('done', len(dups), 'dup groups')


if __name__ == '__main__':
    main()
