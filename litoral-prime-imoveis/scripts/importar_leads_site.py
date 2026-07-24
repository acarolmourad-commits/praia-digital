"""
Litoral Prime — importa automaticamente leads do site para metricas.csv.
Evita que leads capturados no site caiam no esquecimento.
"""
from pathlib import Path
import csv, datetime

BASE = Path(__file__).resolve().parent.parent
LEADS_SITE = BASE / "outreach" / "leads-site.csv"
METRICAS = BASE / "outreach" / "metricas.csv"

TIPO_MAP = {
    "comprar": "Compra",
    "alugar": "Aluguel",
    "vender": "Venda",
    "avaliacao": "Avaliação",
}


def run():
    if not LEADS_SITE.exists():
        print("leads-site.csv não encontrado.")
        return
    with LEADS_SITE.open(newline="", encoding="utf-8") as f:
        site_rows = list(csv.DictReader(f))
    if not site_rows:
        print("Nenhum lead novo no site.")
        return

    existing = []
    if METRICAS.exists():
        with METRICAS.open(newline="", encoding="utf-8") as f:
            existing = list(csv.DictReader(f))
    exist_keys = {(r.get("data"), r.get("nome"), r.get("telefone"), r.get("tipo")) for r in existing}

    today = datetime.date.today().isoformat()
    new_rows = []
    for r in site_rows:
        nome = (r.get("nome") or "").strip()
        telefone = (r.get("telefone") or "").strip()
        interesse = (r.get("interesse") or "").strip().lower()
        tipo = TIPO_MAP.get(interesse, interesse.title() or "Compra")
        mensagem = (r.get("mensagem") or "").strip()
        key = (today, nome, telefone, tipo)
        if key in exist_keys:
            continue
        new_rows.append({
            "data": today,
            "nome": nome,
            "telefone": telefone,
            "cidade": "",
            "tipo": tipo,
            "canal": "site",
            "estagio": "primeiro_contato",
            "acao": "enviar",
            "status": "novo",
            "observacoes": f"Lead do site. {mensagem}" if mensagem else "Lead do site",
        })

    if not new_rows:
        print("Nenhum lead novo para importar.")
        return

    combined = existing + new_rows
    with METRICAS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["data","nome","telefone","cidade","tipo","canal","estagio","acao","status","observacoes"])
        writer.writeheader()
        for r in combined:
            writer.writerow(r)
    print(f"Importados {len(new_rows)} leads do site para metricas.csv")


if __name__ == "__main__":
    run()
