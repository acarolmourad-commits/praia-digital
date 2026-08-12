"""
Backup de métricas da Litoral Prime Imóveis.

Fonte primária:
- outreach/metricas.csv
- docs/chat-log-litoral-prime.json
- docs/relatorio-diario-litoral-prime.html
- docs/leads-litoral-prime.csv, se existir
- outreach/leads-site.csv, se existir
- outreach/do-dia/*/*.csv

Destino:
- backups/metricas/<YYYYMMDD_HHMMSS>/

Política:
- Um snapshot por execução, com timestamp.
- Não remove backups antigos automaticamente.
- Não sobrescreve backups existentes.
- Não imprime segredos.
"""
import csv
import json
import hashlib
import shutil
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parent.parent
SOURCES = [
    BASE / 'outreach' / 'metricas.csv',
    BASE / 'docs' / 'chat-log-litoral-prime.json',
    BASE / 'docs' / 'relatorio-diario-litoral-prime.html',
    BASE / 'docs' / 'leads-litoral-prime.csv',
    BASE / 'outreach' / 'leads-site.csv',
]

# Include outreach do-dia CSVs
do_dia = BASE / 'outreach' / 'do-dia'
if do_dia.exists():
    for day_dir in sorted(do_dia.iterdir()):
        if day_dir.is_dir():
            SOURCES.extend(sorted(day_dir.glob('*.csv')))

now = datetime.now()
stamp = now.strftime('%Y%m%d_%H%M%S')
dest_root = BASE / 'backups' / 'metricas' / stamp
dest_root.mkdir(parents=True, exist_ok=False)

manifest = {
    'project': 'litoral-prime-imoveis',
    'backup_at': now.isoformat(),
    'sources': [],
    'count': 0,
    'size_bytes': 0,
}

copied = 0
errors = []

for src in SOURCES:
    if not src.exists():
        continue
    try:
        rel = src.relative_to(BASE)
        dest = dest_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        copied += 1
        manifest['sources'].append({
            'source': str(rel),
            'size_bytes': src.stat().st_size,
            'sha256': hashlib.sha256(src.read_bytes()).hexdigest(),
        })
    except Exception as exc:  # pragma: no cover
        errors.append(f"{src}: {exc}")

manifest['count'] = copied
manifest['size_bytes'] = sum(item['size_bytes'] for item in manifest['sources'])
manifest_path = dest_root / 'manifest.json'
manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')

if errors:
    print(f'Backup concluído com avisos: {copied} arquivos em {dest_root}')
    for err in errors:
        print(f'Aviso: {err}')
    raise SystemExit(1)

print(f'Backup criado: {dest_root}')
print(f'Arquivos: {copied}')
print(f'Tamanho: {manifest["size_bytes"]} bytes')
print(f'Manifest: {manifest_path}')
