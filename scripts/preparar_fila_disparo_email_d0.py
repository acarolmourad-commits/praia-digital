import csv
from pathlib import Path
from datetime import datetime

FIELDS = [
    "id","nome","email","cidade","bairro","perfil","interesse","mensagem","origem","status","score","data_captura","data_aprovacao"
]
CAPTURE_SRC = Path("docs/sales/leads-captura-site-2026-08-26.csv")
CALC_SRC = Path("docs/sales/leads-calculadora-2026-08-26.csv")
OUT = Path("docs/sales/fila-disparo-email-d0-2026-08-26.csv")

def score(row):
    s = 0
    cidade = (row.get("cidade") or "").strip()
    origem = (row.get("origem") or "").strip()
    perfil = (row.get("perfil") or "").strip()
    interesse = (row.get("interesse") or "").strip()
    mensagem = (row.get("mensagem") or "").strip()

    if cidade in ("Guarujá", "São Vicente"):
        s += 30
    if origem:
        s += 10
    if perfil:
        s += 10
    if interesse:
        s += 10
    if mensagem:
        s += 10
    return min(s, 100)

def valid(row):
    email=(row.get("email") or "").strip().lower()
    if not email or "@" not in email:
        return False
    domain=email.split("@")[-1]
    if "." not in domain:
        return False
    placeholders=["exemplo.com","teste.com","localhost","example.com"]
    if any(email.endswith(p) for p in placeholders):
        return False
    return True

def normalize(row, source):
    r = dict(row)
    r.setdefault("nome", "")
    r.setdefault("mensagem", "")
    r.setdefault("perfil", "")
    r.setdefault("interesse", "")
    if source == "captura":
        r["origem"] = r.get("origem") or "captura-leads-litoral-2026"
    elif source == "calculadora":
        r["origem"] = r.get("origem") or "calculadora-rendimento-temporada-2026"
        r["perfil"] = r.get("perfil") or "Proprietário"
        r["interesse"] = r.get("interesse") or "Aluguel temporada"
    return r

if __name__ == "__main__":
    rows = []
    sources = []

    if CAPTURE_SRC.exists():
        with CAPTURE_SRC.open(newline='', encoding='utf-8') as f:
            rows.extend([normalize(r, "captura") for r in csv.DictReader(f, delimiter=';')])
            sources.append("captura")

    if CALC_SRC.exists():
        with CALC_SRC.open(newline='', encoding='utf-8') as f:
            rows.extend([normalize(r, "calculadora") for r in csv.DictReader(f, delimiter=';')])
            sources.append("calculadora")

    seen = {}
    approved = []
    for r in rows:
        if not valid(r):
            continue
        key = (r.get("email","").strip().lower(), r.get("cidade","").strip(), r.get("bairro","").strip())
        if key in seen:
            continue
        seen[key] = True
        r["score"] = score(r)
        r["status"] = "aprovado"
        r["data_aprovacao"] = datetime.now().isoformat()[:10]
        approved.append(r)

    approved.sort(key=lambda r: (r.get("score",0), r.get("data_captura","")), reverse=True)

    with OUT.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, delimiter=';')
        w.writeheader()
        w.writerows(approved)

    print("SOURCES", sources)
    print("TOTAL_RECEIVED", len(rows))
    print("TOTAL_APPROVED", len(approved))
    print("OUT", OUT)
