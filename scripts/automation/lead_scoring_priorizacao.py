#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lead scoring e priorização automática
Entrada: docs/sales/leads-litoral-enriquecido.csv
Saída: docs/sales/lead-scoring-ranking-praia-digital-2026-07-11.md
"""
import os, csv
from datetime import datetime
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IN = os.path.join(BASE, "docs", "sales", "leads-litoral-enriquecido.csv")
OUT = os.path.join(BASE, "docs", "sales", "lead-scoring-ranking-praia-digital-2026-07-11.md")

if not os.path.exists(IN):
    raise FileNotFoundError(IN)

rows = []
with open(IN, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=",")
    for r in reader:
        rows.append(r)

fields = {
    "perfil": {"construtora": 4, "imobiliaria": 3, "gestor": 2, "corretor": 1},
    "status": {"interessado": 4, "negociando": 3, "parceria_fechada": 2, "resposta_recebida": 2, "contato_enviado": 1, "novo": 1},
    "orcamento": {"R$ 3-5k/mês": 4, "R$ 1-3k/mês": 3, "R$ 500-1k/mês": 2, "R$ 0-500": 1},
}

def score_row(r):
    perfil = fields["perfil"].get((r.get("perfil") or "").strip().lower(), 0)
    status_raw = (r.get("status") or "").strip().lower()
    status = fields["status"].get(status_raw, 1 if status_raw == "" else 0)
    dor = len((r.get("dor_principal") or "").strip().split(","))
    tm = (r.get("tom") or "").strip().lower()
    tom = 2 if tm == "parceiro" else 0
    try:
        pts = int((r.get("pontuacao_lead") or "0").strip())
    except:
        pts = 0
    return perfil + status + dor + tom + max(0, pts // 10)

for r in rows:
    r["__score"] = score_row(r)

rows.sort(key=lambda r: int(r["__score"]), reverse=True)

with open(OUT, "w", encoding="utf-8") as f:
    f.write("# Lead Scoring & Priorização\n\n")
    f.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
    f.write(f"Total de leads: {len(rows)}\n\n")
    f.write("## Ranking\n\n")
    f.write("| # | Lead | Cidade | Contato | Status | Perfil | Score | Pts Lead | Próxima ação |\n")
    f.write("|---|------|--------|---------|--------|--------|-------|----------|--------------|\n")
    for i, r in enumerate(rows[:120], 1):
        next_action = "enviar_proposta" if int(r["__score"]) >= 18 else "demo_15min" if int(r["__score"]) >= 14 else "follow_up"
        f.write(f"| {i} | {r.get('nome_da_imobiliaria','')} | {r.get('cidade','')} | {r.get('pessoa_de_contato','')} | {r.get('status','')} | {r.get('perfil','')} | {r['__score']} | {r.get('pontuacao_lead','')} | {next_action} |\n")

    counts = Counter(r["cidade"].strip() for r in rows if r.get("cidade"))
    f.write("\n## Por cidade\n\n")
    for city, cnt in counts.most_common():
        f.write(f"- {city}: {cnt}\n")

    counts_perfil = Counter((r.get("perfil") or "").strip().lower() for r in rows)
    f.write("\n## Por perfil\n\n")
    for k, v in counts_perfil.most_common():
        if k:
            f.write(f"- {k}: {v}\n")

print(f"Gerado: {OUT}")
print(f"Registros: {len(rows)}")
