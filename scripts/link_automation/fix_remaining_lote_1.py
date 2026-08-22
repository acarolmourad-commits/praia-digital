"""Clean remaining duplicate occurrences from Lote 1 without double-prefixing."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital')
BATCH_LOG = BASE / 'scripts/link_automation/batch-log.json'
ROLLBACK_DIR = BASE / 'scripts/link_automation/rollbacks'
REPORT = BASE / 'scripts/link_automation/link-repair-lote-1-report.json'

REMAINING = [
    ('anfitrioes/central-airbnb.html', 'diagnosticos-anfitrioes.html', 'anfitrioes/diagnosticos-anfitrioes.html'),
    ('anfitrioes/central-booking.html', 'diagnosticos-anfitrioes.html', 'anfitrioes/diagnosticos-anfitrioes.html'),
    ('anfitrioes/central-priceplabs.html', 'diagnosticos-anfitrioes.html', 'anfitrioes/diagnosticos-anfitrioes.html'),
    ('anfitrioes/central-stays.html', 'diagnosticos-anfitrioes.html', 'anfitrioes/diagnosticos-anfitrioes.html'),
]


def sha256_file(path: Path) -> str:
    if not path.exists():
        return ''
    return hashlib.sha256(path.read_bytes()).hexdigest()


batch_id = 'lote-1-rem-' + datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
applied = []
for src_rel, old, new in REMAINING:
    src = BASE / src_rel
    if not src.exists():
        continue
    text = src.read_text(encoding='utf-8', errors='ignore')
    # Only replace occurrences that are NOT already prefixed correctly
    safe_new = new.replace('\\', '/')
    if old not in text:
        continue
    before_hash = sha256_file(src)
    rollback_path = ROLLBACK_DIR / f"{batch_id}__{src_rel.replace('/', '__').replace('.', '_')}.txt"
    rollback_path.write_text(text, encoding='utf-8')
    # Replace remaining old hrefs that are not already part of safe_new
    new_text = text.replace(old, safe_new)
    # Fix any double-prefix just in case
    new_text = new_text.replace('anfitrioes/anfitrioes/', 'anfitrioes/')
    new_text = new_text.replace('anfitrioes/anfitrioes/', 'anfitrioes/')
    if new_text == text:
        continue
    src.write_text(new_text, encoding='utf-8')
    after_hash = sha256_file(src)
    if before_hash == after_hash:
        continue
    applied.append({
        'batch_id': batch_id,
        'source': src_rel,
        'original_href': old,
        'new_href': safe_new,
        'result': 'APPLIED',
        'hash_before': before_hash,
        'hash_after': after_hash,
    })

out = {
    'batch_id': batch_id,
    'timestamp': datetime.now(timezone.utc).isoformat(),
    'applied': len(applied),
    'details': applied,
}
REPORT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
batch_log = json.loads(BATCH_LOG.read_text(encoding='utf-8')) if BATCH_LOG.exists() else []
batch_log.append(out)
BATCH_LOG.write_text(json.dumps(batch_log, ensure_ascii=False, indent=2), encoding='utf-8')
print('applied=', len(applied))
for a in applied:
    print(a['source'], a['original_href'], '->', a['new_href'])
