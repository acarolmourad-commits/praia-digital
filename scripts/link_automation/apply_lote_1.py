"""Apply Lote 1: exactly 21 deterministic REPARAR candidates."""
from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital')
REPORT = BASE / 'scripts/link_automation/dry-run-report.json'
BATCH_LOG = BASE / 'scripts/link_automation/batch-log.json'
ROLLBACK_DIR = BASE / 'scripts/link_automation/rollbacks'
OUT_JSON = BASE / 'scripts/link_automation/link-repair-lote-1-report.json'
OUT_CSV = BASE / 'scripts/link_automation/link-repair-lote-1.csv'

ROLLBACK_DIR.mkdir(parents=True, exist_ok=True)
report = json.loads(REPORT.read_text(encoding='utf-8'))
seen = set()
unique_cands = []
for c in report['batch']['candidates']:
    if c['status'] == 'REPARAR' and c['target_href']:
        key = (c['source'], c['original_href'], c['target_href'])
        if key not in seen:
            seen.add(key)
            unique_cands.append(c)
cands = unique_cands
batch_id = 'lote-1-' + datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
applied = []
skipped = []
errors = []


def sha256_file(path: Path) -> str:
    if not path.exists():
        return ''
    return hashlib.sha256(path.read_bytes()).hexdigest()


for c in cands:
    src = BASE / c['source']
    old = c['original_href']
    new = c['target_href'].replace('\\', '/')
    if not src.exists():
        errors.append({**c, 'erro': 'source_missing', 'result': 'ERROR'})
        continue
    text = src.read_text(encoding='utf-8', errors='ignore')
    if old not in text:
        skipped.append({**c, 'result': 'SKIPPED_LINK_NOT_FOUND'})
        continue
    before_hash = sha256_file(src)
    safe_rel = c['source'].replace('/', '__').replace('\\', '__').replace('.', '_')
    rollback_path = ROLLBACK_DIR / f"{batch_id}__{safe_rel}.txt"
    rollback_path.write_text(text, encoding='utf-8')
    new_text = text.replace(old, new)
    if new_text == text:
        skipped.append({**c, 'result': 'SKIPPED_NO_CHANGE'})
        continue
    src.write_text(new_text, encoding='utf-8')
    after_hash = sha256_file(src)
    if before_hash == after_hash:
        skipped.append({**c, 'result': 'SKIPPED_WRITE_NO_CHANGE'})
        continue
    applied.append({
        'batch_id': batch_id,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'dry_run': False,
        'source': c['source'],
        'original_href': old,
        'new_href': new,
        'rule': c.get('pattern_matched'),
        'confidence': c.get('confidence'),
        'evidence': c.get('evidence'),
        'hash_before': before_hash,
        'hash_after': after_hash,
        'result': 'APPLIED',
    })

out = {
    'batch_id': batch_id,
    'timestamp': datetime.now(timezone.utc).isoformat(),
    'dry_run': False,
    'total_candidates': len(cands),
    'applied': len(applied),
    'skipped': len(skipped),
    'errors': len(errors),
    'details': applied + skipped + errors,
}
OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
with OUT_CSV.open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['batch_id', 'timestamp', 'dry_run', 'source', 'original_href', 'new_href', 'rule', 'confidence', 'evidence', 'hash_before', 'hash_after', 'result'])
    writer.writeheader()
    for row in out['details']:
        writer.writerow({k: row.get(k, '') for k in writer.fieldnames})

batch_log = json.loads(BATCH_LOG.read_text(encoding='utf-8')) if BATCH_LOG.exists() else []
batch_log.append(out)
BATCH_LOG.write_text(json.dumps(batch_log, ensure_ascii=False, indent=2), encoding='utf-8')

print('batch_id=', batch_id)
print('applied=', len(applied))
print('skipped=', len(skipped))
print('errors=', len(errors))
for row in applied:
    print(row['source'], row['original_href'], '->', row['new_href'])
