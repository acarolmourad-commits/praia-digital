from pathlib import Path
from datetime import datetime
import shutil

root = Path("C:/Users/Carolina/praia-digital")
backup_root = root / "backups"
backup_root.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = backup_root / timestamp
backup_dir.mkdir(exist_ok=True)

# Files to backup
files_to_backup = [
    "docs/sales/leads-litoral-enriquecido.csv",
    "docs/sales/leads-litoral-enriquecido-realista.csv",
    "docs/sales/parcerias-leads-capturados.csv",
    "docs/sales/form-tracker-2026-07-12.csv",
    "docs/sales/followup-registro.md",
    "docs/sales/csv-lotes-email/",
]

for item in files_to_backup:
    src = root / item
    if not src.exists():
        continue
    rel = src.relative_to(root)
    dst = backup_dir / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_file():
        shutil.copy2(src, dst)
    elif src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=True)

print(f"Backup criado em: {backup_dir}")
print(f"Total de backups: {len(list(backup_root.iterdir()))}")
