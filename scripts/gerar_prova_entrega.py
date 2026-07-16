#!/usr/bin/env python3
"""Gera relatorio de PROVA DE ENTREGA (auditoria) do outbound proprietarios autogestores.
Le os trackers WPP+e-mail e produz:
  - docs/sales/prova-entrega-outbound.json   (log estruturado)
  - docs/sales/prova-entrega-outbound.html   (relatorio visual)
Mostra, por canal, quantas Msg1/2/2.5/3 e E1/2/3 ja foram enviadas (status != pendente)
e quais lotes ja tiveram o primeiro toque.
"""
import csv, os, json, glob, re
from collections import defaultdict
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
DIR = os.path.join(REPO, "docs/sales/csv-lotes-email")
JSON_OUT = os.path.join(REPO, "docs/sales", "prova-entrega-outbound.json")
HTML_OUT = os.path.join(REPO, "docs/sales", "prova-entrega-outbound.html")
PAD_W = re.compile(r"lote-whatsapp-proprietarios-(\d+)-(\d{4}-\d{2}-\d{2})\.csv")
PAD_E = re.compile(r"lote-email-proprietarios-(\d+)-(\d{4}-\d{2}-\d{2})\.csv")

STATUS_ENVIADOS = {"enviado_msg1","enviado_msg2","enviado_msg3","respondeu","fechou",
                   "enviado_email1","enviado_email2","enviado_email3"}

def contar(arq, tipo):
    # tipo 'wpp' ou 'email' — olha coluna Status nos CSVs de lote
    passos = ["1","2","2.5","3"] if tipo=="wpp" else ["1","2","3"]
    cnt = defaultdict(int); total = 0
    rows = list(csv.DictReader(open(arq, encoding="utf-8-sig"), delimiter=";"))
    total = len(rows)
    for r in rows:
        st = r.get("Status","")
        if st in STATUS_ENVIADOS:
            # conta o passo mais avancado atingido
            if st.startswith("enviado_msg") or st.startswith("enviado_email"):
                passo = st[-1]
                cnt[passo] += 1
            elif st == "respondeu":
                cnt["resp"] += 1
            elif st == "fechou":
                cnt["fech"] += 1
    return total, cnt

def main():
    rel = {"data": date.today().isoformat(), "canais": {}}
    for label, pad, prefix, tipo in [("WhatsApp", PAD_W, "whatsapp", "wpp"), ("E-mail", PAD_E, "email", "email")]:
        lotes = {}
        for arq in sorted(glob.glob(os.path.join(DIR, f"lote-{prefix}-proprietarios-*.csv"))):
            m = pad.search(os.path.basename(arq))
            if not m: continue
            lote = m.group(1); total, cnt = contar(arq, tipo)
            lotes[lote] = {"total": total, "enviados_primeiro": cnt.get("1",0),
                           "enviados_segundo": cnt.get("2",0), "enviados_prova": cnt.get("2.5",0),
                           "enviados_terceiro": cnt.get("3",0), "respondeu": cnt.get("resp",0),
                           "fechou": cnt.get("fech",0)}
        rel["canais"][label] = {"lotes": lotes,
            "total_leads": sum(v["total"] for v in lotes.values()),
            "primeiro_toque": sum(v["enviados_primeiro"] for v in lotes.values())}
    json.dump(rel, open(JSON_OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    # HTML
    linhas = []
    for canal, dados in rel["canais"].items():
        linhas.append(f'<h2 style="color:#fff;">{canal} — {dados["total_leads"]} leads · 1º toque: {dados["primeiro_toque"]}</h2>')
        linhas.append('<table style="width:100%;border-collapse:collapse;color:#e2e8f0;margin-bottom:1.5rem;">'
            '<tr><th style="text-align:left;padding:6px;border-bottom:2px solid #1e3a5f;color:#94a3b8;">Lote</th>'
            '<th style="text-align:right;padding:6px;border-bottom:2px solid #1e3a5f;color:#94a3b8;">Leads</th>'
            '<th style="text-align:right;padding:6px;border-bottom:2px solid #1e3a5f;color:#94a3b8;">Msg1/E1</th>'
            '<th style="text-align:right;padding:6px;border-bottom:2px solid #1e3a5f;color:#94a3b8;">Msg2/E2</th>'
            '<th style="text-align:right;padding:6px;border-bottom:2px solid #1e3a5f;color:#94a3b8;">Resp</th>'
            '<th style="text-align:right;padding:6px;border-bottom:2px solid #1e3a5f;color:#94a3b8;">Fechou</th></tr>')
        for lote, v in sorted(dados["lotes"].items(), key=lambda x: int(x[0])):
            linhas.append(f'<tr><td style="padding:6px;border-bottom:1px solid #1e3a5f;">{lote}</td>'
                f'<td style="padding:6px;border-bottom:1px solid #1e3a5f;text-align:right;">{v["total"]}</td>'
                f'<td style="padding:6px;border-bottom:1px solid #1e3a5f;text-align:right;color:#22d3ee;">{v["enviados_primeiro"]}</td>'
                f'<td style="padding:6px;border-bottom:1px solid #1e3a5f;text-align:right;">{v["enviados_segundo"]}</td>'
                f'<td style="padding:6px;border-bottom:1px solid #1e3a5f;text-align:right;">{v["respondeu"]}</td>'
                f'<td style="padding:6px;border-bottom:1px solid #1e3a5f;text-align:right;color:#4ade80;">{v["fechou"]}</td></tr>')
        linhas.append('</table>')
    html = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Prova de Entrega — Outbound Praia Digital</title></head><body style="margin:0;font-family:Segoe UI,Arial,sans-serif;background:#07111f;color:#e2e8f0;"><div style="max-width:900px;margin:0 auto;padding:2rem;"><h1 style="color:#fff;">✅ Prova de Entrega — Outbound</h1><p style="color:#94a3b8;">Auditoria de disparos · {date.today():%d/%m/%Y} · Praia Digital</p>{''.join(linhas)}<p style="color:#64748b;margin-top:2rem;font-size:.8rem;">Fonte: lotes WhatsApp/e-mail + trackers. Log: prova-entrega-outbound.json</p></div></body></html>"""
    open(HTML_OUT, "w", encoding="utf-8").write(html)
    print(f"Prova de entrega: {HTML_OUT}\nJSON: {JSON_OUT}\nCanais: {list(rel['canais'].keys())}")

if __name__ == "__main__":
    main()
