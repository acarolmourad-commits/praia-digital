"""
Litoral Prime — captura leads do site em outreach/leads-site.csv
"""
from pathlib import Path
import csv, datetime

BASE = Path(__file__).resolve().parent.parent
LEADS_FILE = BASE / "outreach" / "leads-site.csv"
FIELDS = ["data", "nome", "email", "telefone", "interesse", "mensagem"]

LEADS_FILE.parent.mkdir(parents=True, exist_ok=True)


def save(data: dict):
    exists = LEADS_FILE.exists()
    with LEADS_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow({k: data.get(k, "") for k in FIELDS})

if __name__ == "__main__":
    import sys
    save({
        "data": datetime.date.today().isoformat(),
        "nome": sys.argv[1] if len(sys.argv) > 1 else "",
        "email": sys.argv[2] if len(sys.argv) > 2 else "",
        "telefone": sys.argv[3] if len(sys.argv) > 3 else "",
        "interesse": sys.argv[4] if len(sys.argv) > 4 else "",
        "mensagem": sys.argv[5] if len(sys.argv) > 5 else "",
    })
