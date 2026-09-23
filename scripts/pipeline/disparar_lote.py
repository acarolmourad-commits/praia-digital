"""disparar_lote.py — gera CSVs de disparo e ATUALIZA last_contact (substitui disparar_lote_*.py).

CORRECAO PRINCIPAL vs. scripts antigos: apos gerar os arquivos de disparo,
atualiza o campo last_contact do lead no tracker master, destravando o funil
(antes os leads ficavam eternamente em pendente_msg1/pendente_q1).

Uso:
    python scripts/pipeline/disparar_lote.py --segmento automacao
"""
import argparse, csv, os
from datetime import datetime

REPO = os.environ.get("PRAIA_REPO", "C:/Users/Carolina/praia-digital")
LOTES_DIR = f"{REPO}/docs/sales/csv-lotes-b2b"
TRACKER_MASTER = f"{LOTES_DIR}/tracker-master.csv"

def disparar(segmento: str, data: str) -> int:
    sanitizado = f"{LOTES_DIR}/lote-b2b-{segmento}-sanitizado-{data}.csv"
    if not os.path.exists(sanitizado):
        print(f"[SKIP] {segmento}: sanitizado nao encontrado: {sanitizado}")
        return 0
    with open(sanitizado, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys()) if rows else []
    whats = f"{LOTES_DIR}/para-whatsapp-{segmento}-{data}.csv"
    brevo = f"{LOTES_DIR}/para-brevo-{segmento}-{data}.csv"
    for dest, campo in ((whats, "whatsapp"), (brevo, "email")):
        alvo = [r for r in rows if (r.get(campo) or "").strip()]
        with open(dest, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames); w.writeheader(); w.writerows(alvo)
    checklist = f"{REPO}/docs/sales/checklist-envio-{segmento}-{data}.txt"
    with open(checklist, "w", encoding="utf-8") as f:
        f.write(f"Checklist {segmento} {data}\n- WhatsApp: {whats}\n- E-mail (Brevo): {brevo}\n")

    # === Atualiza tracker master + last_contact (o passo que faltava) ===
    hoje_br = datetime.now().strftime("%d/%m/%Y")
    master, mfields = [], ["segmento", "nome", "email", "whatsapp", "status", "last_contact", "updated_at"]
    if os.path.exists(TRACKER_MASTER):
        with open(TRACKER_MASTER, newline="", encoding="utf-8") as f:
            r = csv.DictReader(f); master = list(r); mfields = r.fieldnames or mfields
    idx = {(m.get("email") or m.get("whatsapp")): m for m in master}
    for row in rows:
        chave = (row.get("email") or row.get("whatsapp") or "").strip().lower()
        reg = idx.get(chave, {k: "" for k in mfields})
        reg.update({"segmento": segmento, "nome": row.get("nome", ""), "email": row.get("email", ""),
                    "whatsapp": row.get("whatsapp", ""), "status": "msg1_enviada",
                    "last_contact": hoje_br, "updated_at": datetime.now().isoformat()})
        idx[chave] = reg
    with open(TRACKER_MASTER, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=mfields); w.writeheader(); w.writerows(idx.values())
    print(f"Pronto: {len(rows)} leads | tracker-master atualizado ({len(idx)} registros)")
    return len(rows)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--segmento", required=True)
    p.add_argument("--data", default=datetime.now().strftime("%Y-%m-%d"))
    a = p.parse_args()
    disparar(a.segmento, a.data)
