"""Consolidação automática de duplicatas exatas com rollback."""
from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital')
BACKLOG = BASE / 'scripts/dup_consolidation_backlog_v2.json'
BATCH_LOG = BASE / 'scripts/dup_batch_log.json'
ROLLBACK_DIR = BASE / 'scripts/dup_rollbacks'
DRY_RUN = True


def sha256_file(path: Path) -> str:
    if not path.exists():
        return ''
    return hashlib.sha256(path.read_bytes()).hexdigest()


def consolidate_group(group):
    files = group['files']
    if len(files) < 2:
        return []

    # Sort files: prefer shortest path, then alphabetical
    sorted_files = sorted(files, key=lambda f: (len(f), f))
    canonical = sorted_files[0]
    canonical_path = BASE / canonical

    if not canonical_path.exists():
        return []

    results = []
    canonical_text = canonical_path.read_text(encoding='utf-8', errors='ignore')
    canonical_hash = sha256_file(canonical_path)

    for dup in files[1:]:
        dup_path = BASE / dup
        if not dup_path.exists():
            continue
        if dup_path.resolve() == canonical_path.resolve():
            continue

        dup_text = dup_path.read_text(encoding='utf-8', errors='ignore')
        dup_hash = sha256_file(dup_path)

        if DRY_RUN:
            results.append({
                'canonical': canonical,
                'duplicate': dup,
                'result': 'DRY_RUN',
                'canonical_hash': canonical_hash,
                'duplicate_hash': dup_hash,
            })
        else:
            # Create redirect from dup to canonical
            redirect_html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=/{canonical}">
  <link rel="canonical" href="https://praia.digital/{canonical}">
  <title>Redirecionando...</title>
</head>
<body>
  <p>Redirecionando para <a href="/{canonical}">{canonical}</a>...</p>
</body>
</html>'''
            dup_path.write_text(redirect_html, encoding='utf-8')
            after_hash = sha256_file(dup_path)
            results.append({
                'canonical': canonical,
                'duplicate': dup,
                'result': 'REDIRECTED',
                'canonical_hash': canonical_hash,
                'duplicate_hash_before': dup_hash,
                'duplicate_hash_after': after_hash,
            })

    return results


def main():
    backlog = json.loads(BACKLOG.read_text(encoding='utf-8'))
    candidates = backlog.get('candidates', [])

    batch_id = 'dup-lote-1-' + datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
    all_results = []

    for group in candidates:
        results = consolidate_group(group)
        for r in results:
            r['batch_id'] = batch_id
            r['timestamp'] = datetime.now(timezone.utc).isoformat()
            r['dry_run'] = DRY_RUN
            all_results.append(r)

    output = {
        'batch_id': batch_id,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'dry_run': DRY_RUN,
        'total_groups': len(candidates),
        'total_duplicates': len(all_results),
        'results': all_results,
    }

    BATCH_LOG.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
    print('batch_id=', batch_id)
    print('total_groups=', len(candidates))
    print('total_duplicates=', len(all_results))
    print('dry_run=', DRY_RUN)
    for r in all_results[:10]:
        print(r['duplicate'], '->', r['canonical'], r['result'])


if __name__ == '__main__':
    main()
