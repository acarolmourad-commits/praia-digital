"""Rollback/lot management for link automation."""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital')
BATCH_LOG = BASE / 'scripts/link_automation/batch-log.json'
ROLLBACK_DIR = BASE / 'scripts/link_automation/rollbacks'


def append_batch(record: dict) -> None:
    BATCH_LOG.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads(BATCH_LOG.read_text(encoding='utf-8')) if BATCH_LOG.exists() else []
    data.append(record)
    BATCH_LOG.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def save_rollback_snapshot(batch_id: str, file_rel: str, original_text: str) -> None:
    ROLLBACK_DIR.mkdir(parents=True, exist_ok=True)
    path = ROLLBACK_DIR / f'{batch_id}__{file_rel.replace("/", "__").replace(".", "_")}.txt'
    path.write_text(original_text, encoding='utf-8')


def rollback(batch_id: str) -> dict:
    if not BATCH_LOG.exists():
        return {'status': 'error', 'message': 'batch-log.json not found'}
    data = json.loads(BATCH_LOG.read_text(encoding='utf-8'))
    batch = next((b for b in data if b.get('batch_id') == batch_id and not b.get('dry_run')), None)
    if not batch:
        return {'status': 'error', 'message': 'batch not found or is dry-run'}
    restored = 0
    errors = 0
    for c in batch.get('candidates', []):
        if not c.get('applied'):
            continue
        path = BASE / c['source']
        snapshot = ROLLBACK_DIR / f"{batch_id}__{c['source'].replace('/', '__').replace('.', '_')}.txt"
        if snapshot.exists():
            path.write_text(snapshot.read_text(encoding='utf-8'), encoding='utf-8')
            restored += 1
        else:
            errors += 1
    return {'status': 'ok', 'restored': restored, 'errors': errors}


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python link_automation/rollback.py <batch_id>')
        sys.exit(1)
    print(rollback(sys.argv[1]))
