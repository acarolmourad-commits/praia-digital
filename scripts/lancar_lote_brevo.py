#!/usr/bin/env python3
from pathlib import Path
import webbrowser
import subprocess
import sys

BASE = Path("C:/Users/Carolina/praia-digital")
CSV = BASE / "csv-lotes-email" / "lote-brevo-30-2026-07-10.csv"
BREVO_IMPORT_URL = "https://app.brevo.com/contacts/import"

if not CSV.exists():
    print(f"CSV não encontrado: {CSV}")
    sys.exit(1)

print("Abrindo CSV e página de importação do Brevo...")
webbrowser.open(BREVO_IMPORT_URL)

if sys.platform.startswith("win"):
    subprocess.run(["start", str(CSV)], shell=True)
elif sys.platform.startswith("darwin"):
    subprocess.run(["open", str(CSV)])
else:
    subprocess.run(["xdg-open", str(CSV)])
