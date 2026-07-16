#!/usr/bin/env python3
"""Gera dashboard HTML de conversao dos lotes EMAIL de proprietarios autogestores."""
import csv, os, re, glob
from collections import Counter, defaultdict
from datetime import date
REPO = r"C:/Users/Carolina/praia-digital"
EMAIL_DIR = os.path.join(REPO, "docs/sales/csv-lotes-email")
TRACKER = os.path.join(EMAIL_DIR, "tracker-email-proprietarios.csv")
OUT = os.path.join(REPO, "docs/sales", "dashboard-email-proprietarios.html")
FUNIL = ["pendente_email1","enviado_email1","enviado_email2","enviado_email3","respondeu","fechou","sem_interesse"]
LABEL = {"pendente_email1":"Pendente E1","enviado_email1":"E1 enviado","enviado_email2":"E2 enviado",
    "enviado_email3":"E3 enviado","respondeu":"Respondeu","fechou":"Fechou","sem_interesse":"Sem interesse"}

def main():
    if not os.path.exists(TRACKER):
        print("Tracker ausente."); return
    rows = list(csv.DictReader(open(TRACKER, encoding="utf-8-sig"), delimiter=";"))
    total = len(rows); cnt = Counter(r["Status"] for r in rows)
    por_cidade = defaultdict(lambda: defaultdict(int))
    for r in rows: por_cidade[r["Cidade"]][r["Status"]] += 1
    fechou = cnt.get("fechou",0); resp = cnt.get("respondeu",0); sem = cnt.get("sem_interesse",0)
    valor = sum(float(r["Valor_Estimado"]) for r in rows if r.get("Valor_Estimado"))
    ativos = total - sem
    def bar(s):
        n = cnt.get(s,0); pct = (n/total*100) if total else 0
        return (f'<div style="display:flex;align-items:center;gap:8px;margin:4px 0;">'
            f'<div style="width:160px;color:#cbd5e1;">{LABEL[s]}</div>'
            f'<div style="flex:1;background:#0f2942;border-radius:6px;overflow:hidden;">'
            f'<div style="width:{pct:.1f}%;background:linear-gradient(90deg,#a78bfa,#6366f1);height:20px;"></div></div>'
            f'<div style="width:70px;text-align:right;color:#e2e8f0;">{n} ({pct:.0f}%)</div></div>')
    c_html = ""
    for cid, st in sorted(por_cidade.items()):
        c_html += (f'<tr><td style="padding:6px;border-bottom:1px solid #1e3a5f;">{cid}</td>'
            f'<td style="padding:6px;border-bottom:1px solid #1e3a5f;text-align:right;">{sum(st.values())}</td>'
            f'<td style="padding:6px;border-bottom:1px solid #1e3a5f;text-align:right;color:#a78bfa;">{st.get("respondeu",0)+st.get("fechou",0)}</td>'
            f'<td style="padding:6px;border-bottom:1px solid #1e3a5f;text-align:right;color:#4ade80;">{st.get("fechou",0)}</td></tr>')
    html = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Dashboard Email — Proprietários Autogestores</title></head><body style="margin:0;font-family:Segoe UI,Arial,sans-serif;background:#07111f;color:#e2e8f0;"><div style="max-width:900px;margin:0 auto;padding:2rem;"><h1 style="color:#fff;">📧 Email — Proprietários Autogestores</h1><p style="color:#94a3b8;">Atualizado em {date.today():%d/%m/%Y} · Praia Digital</p><div style="display:flex;gap:1rem;flex-wrap:wrap;margin:1.5rem 0;"><div style="flex:1;min-width:150px;background:#0f2942;padding:1rem;border-radius:10px;"><div style="font-size:2rem;color:#fff;">{total}</div><div style="color:#94a3b8;">Leads totais</div></div><div style="flex:1;min-width:150px;background:#0f2942;padding:1rem;border-radius:10px;"><div style="font-size:2rem;color:#a78bfa;">{resp+fechou}</div><div style="color:#94a3b8;">Responderam</div></div><div style="flex:1;min-width:150px;background:#0f2942;padding:1rem;border-radius:10px;"><div style="font-size:2rem;color:#4ade80;">{fechou}</div><div style="color:#94a3b8;">Fechados</div></div><div style="flex:1;min-width:150px;background:#0f2942;padding:1rem;border-radius:10px;"><div style="font-size:2rem;color:#facc15;">R$ {valor:,.0f}</div><div style="color:#94a3b8;">Receita estimada</div></div></div><h2 style="color:#fff;">Funil de status</h2>{''.join(bar(s) for s in FUNIL)}<h2 style="color:#fff;margin-top:2rem;">Por cidade</h2><table style="width:100%;border-collapse:collapse;color:#e2e8f0;"><tr><th style="text-align:left;padding:6px;border-bottom:2px solid #1e3a5f;color:#94a3b8;">Cidade</th><th style="text-align:right;padding:6px;border-bottom:2px solid #1e3a5f;color:#94a3b8;">Leads</th><th style="text-align:right;padding:6px;border-bottom:2px solid #1e3a5f;color:#94a3b8;">Resp.</th><th style="text-align:right;padding:6px;border-bottom:2px solid #1e3a5f;color:#94a3b8;">Fechou</th></tr>{c_html}</table><p style="color:#64748b;margin-top:2rem;font-size:.8rem;">Fonte: tracker-email-proprietarios.csv</p></div></body></html>"""
    open(OUT, "w", encoding="utf-8").write(html)
    print(f"Dashboard: {OUT}\nTotal {total} | Responderam {resp+fechou} | Fechados {fechou} | Receita R${valor:,.0f}")

if __name__ == "__main__":
    main()
