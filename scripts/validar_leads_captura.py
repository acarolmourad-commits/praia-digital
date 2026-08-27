import csv
from pathlib import Path

FIELDS = [
    "id","nome","email","cidade","bairro","perfil","interesse","mensagem","origem","status","score","data_captura"
]
OUT = Path("docs/sales/leads-captura-site-2026-08-26.csv")

def score(row):
    s = 0
    if row.get("cidade") in ("Guarujá","São Vicente"):
        s += 30
    if row.get("perfil") in ("Proprietário","Investidor"):
        s += 20
    if row.get("interesse") in ("Venda","Aluguel temporada"):
        s += 20
    if row.get("mensagem"):
        s += 10
    return min(s, 100)

def next_id(path):
    if not path.exists():
        return 1
    with path.open(newline='', encoding='utf-8') as f:
        return sum(1 for _ in csv.DictReader(f, delimiter=';')) + 1

def append(row):
    exists = OUT.exists()
    with OUT.open('a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, delimiter=';')
        if not exists:
            w.writeheader()
        w.writerow(row)

if __name__ == "__main__":
    print("Arquivo:", OUT)
    print("Pronto para receber submissões do formulário.")
