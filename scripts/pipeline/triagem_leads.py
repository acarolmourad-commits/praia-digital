"""triagem_leads.py — limpeza opcional do leads-litoral-enriquecido.csv.

Hoje TODOS os 600 leads tem last_contact = 08/07/2026 (77 dias), porque nenhum
script atualizava esse campo. Este script faz a triagem inicial (rode UMA vez,
com backup automatico):

- status "parceria_fechada" -> mantido (excluido das filas pelo automacao_diaria.py)
- "contato_inicial_enviado" com 45+ dias sem contato -> status "reativar_q1"
  (entra numa unica campanha de reativacao, em vez de follow-up infinito)
- "interessado" -> mantido (fila de call)

Uso:
    python scripts/pipeline/triagem_leads.py --aplicar
"""
import argparse, csv, shutil
from datetime import datetime

LEADS = "docs/sales/leads-litoral-enriquecido.csv"
LIMITE_DIAS = 45

def pdte(s):
    try: return datetime.strptime(str(s).strip(), "%d/%m/%Y")
    except Exception: return None

def run(aplicar: bool):
    with open(LEADS, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f); rows = list(r); fields = r.fieldnames
    agora = datetime.now()
    reativar = 0
    for row in rows:
        last = pdte(row.get("last_contact"))
        dias = (agora - last).days if last else 999
        if row.get("status") == "contato_inicial_enviado" and dias >= LIMITE_DIAS:
            row["status"] = "reativar_q1"; reativar += 1
    print(f"Leads marcados para reativacao: {reativar} de {len(rows)}")
    if aplicar:
        shutil.copy(LEADS, LEADS + ".bak")
        with open(LEADS, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
        print("Arquivo atualizado (backup em .bak).")
    else:
        print("Modo simulacao. Rode com --aplicar para gravar.")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--aplicar", action="store_true")
    a = p.parse_args()
    run(a.aplicar)
