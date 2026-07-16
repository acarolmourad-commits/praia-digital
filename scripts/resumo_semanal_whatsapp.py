#!/usr/bin/env python3
"""
Resumo semanal (domingo) do outbound WhatsApp de proprietarios autogestores.
Consolida tracker, regera dashboard e emite relatorio de ROI no stdout
(entregue via cron no Telegram). Tambem exporta JSON para historico.
"""
import csv, os, json, glob, re
from collections import Counter, defaultdict
from datetime import date, timedelta

REPO = r"C:/Users/Carolina/praia-digital"
WHATS_DIR = os.path.join(REPO, "docs/sales/csv-lotes-email")
TRACKER = os.path.join(WHATS_DIR, "tracker-whatsapp-proprietarios.csv")
OUT_JSON = os.path.join(REPO, "docs/sales", "historico-semanal-whatsapp.json")

STATUS_KEYS = ["pendente_msg1","enviado_msg1","enviado_msg2","enviado_msg3",
               "respondeu","fechou","sem_interesse"]

def main():
    if not os.path.exists(TRACKER):
        print("Tracker ausente. Rode consolidar_tracker_whatsapp.py.")
        return
    rows = list(csv.DictReader(open(TRACKER, encoding="utf-8-sig"), delimiter=";"))
    total = len(rows)
    cnt = Counter(r["Status"] for r in rows)
    resp = cnt.get("respondeu", 0) + cnt.get("fechou", 0)
    fechou = cnt.get("fechou", 0)
    sem = cnt.get("sem_interesse", 0)
    ativos = total - sem
    try:
        valor = sum(float(r["Valor_Estimado"]) for r in rows if r.get("Valor_Estimado"))
    except ValueError:
        valor = 0
    taxa_resp = (resp / ativos * 100) if ativos else 0
    taxa_fech = (fechou / ativos * 100) if ativos else 0

    # lotes participantes
    lotes = sorted({r["Lote"] for r in rows})
    # receita por cidade
    por_cidade = defaultdict(lambda: {"leads":0,"resp":0,"fechou":0,"valor":0.0})
    for r in rows:
        c = por_cidade[r["Cidade"]]
        c["leads"] += 1
        if r["Status"] in ("respondeu","fechou"): c["resp"] += 1
        if r["Status"] == "fechou": c["fechou"] += 1
        try:
            if r.get("Valor_Estimado"): c["valor"] += float(r["Valor_Estimado"])
        except ValueError: pass

    semana = date.today().isocalendar()[1]
    rel = {
        "semana": semana, "data": date.today().isoformat(),
        "total": total, "responderam": resp, "fechados": fechou,
        "sem_interesse": sem, "receita_estimada": valor,
        "taxa_resposta": round(taxa_resp,1), "taxa_fechamento": round(taxa_fech,1),
        "lotes": lotes
    }
    historico = []
    if os.path.exists(OUT_JSON):
        try: historico = json.load(open(OUT_JSON, encoding="utf-8"))
        except: historico = []
    historico.append(rel)
    json.dump(historico, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    # monta saida
    linhas = []
    linhas.append(f"📈 RESUMO SEMANAL — WhatsApp Proprietários (sem {semana})")
    linhas.append(f"Data: {date.today():%d/%m/%Y}")
    linhas.append(f"Leads ativos: {ativos} (de {total} | {sem} sem interesse)")
    linhas.append(f"Responderam: {resp} ({taxa_resp:.1f}%)")
    linhas.append(f"Fechados: {fechou} ({taxa_fech:.1f}%)")
    linhas.append(f"Receita estimada: R$ {valor:,.0f}")
    linhas.append(f"Lotes: {', '.join(lotes)}")
    linhas.append("\nPor cidade:")
    for cid, c in sorted(por_cidade.items()):
        linhas.append(f"  • {cid}: {c['leads']} leads | {c['resp']} resp | "
                      f"{c['fechou']} fechou | R$ {c['valor']:,.0f}")
    linhas.append("\nDashboard: docs/sales/dashboard-whatsapp-proprietarios.html")
    linhas.append("Histórico: docs/sales/historico-semanal-whatsapp.json")
    print("\n".join(linhas))

if __name__ == "__main__":
    main()
