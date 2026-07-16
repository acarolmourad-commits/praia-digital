#!/usr/bin/env python3
"""Gera dashboard HTML CONSOLIDADO (WhatsApp + Email) dos proprietarios autogestores."""
import csv, os
from collections import defaultdict
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
DIR = os.path.join(REPO, "docs/sales/csv-lotes-email")
OUT = os.path.join(REPO, "docs/sales", "dashboard-outbound-proprietarios.html")

CANAIS = {
    "WhatsApp": {
        "tracker": os.path.join(DIR, "tracker-whatsapp-proprietarios.csv"),
        "resp": ("respondeu","fechou"), "fechou": ("fechou",), "cor": "#22d3ee"
    },
    "E-mail": {
        "tracker": os.path.join(DIR, "tracker-email-proprietarios.csv"),
        "resp": ("respondeu","fechou"), "fechou": ("fechou",), "cor": "#a78bfa"
    }
}

def ler(tracker):
    if not os.path.exists(tracker): return []
    return list(csv.DictReader(open(tracker, encoding="utf-8-sig"), delimiter=";"))

def main():
    res = {}
    for canal, cfg in CANAIS.items():
        rows = ler(cfg["tracker"])
        total = len(rows)
        cnt = defaultdict(int)
        for r in rows: cnt[r["Status"]] += 1
        resp = sum(cnt[s] for s in cfg["resp"])
        fechou = sum(cnt[s] for s in cfg["fechou"])
        sem = cnt.get("sem_interesse",0)
        valor = sum(float(r["Valor_Estimado"]) for r in rows if r.get("Valor_Estimado"))
        ativos = total - sem
        tx_resp = (resp/ativos*100) if ativos else 0
        tx_fech = (fechou/ativos*100) if ativos else 0
        res[canal] = dict(total=total, resp=resp, fechou=fechou, valor=valor,
                          tx_resp=tx_resp, tx_fech=tx_fech, cor=cfg["cor"])
    tot_leads = sum(v["total"] for v in res.values())
    tot_fech = sum(v["fechou"] for v in res.values())
    tot_valor = sum(v["valor"] for v in res.values())

    cards = ""
    for canal, v in res.items():
        cards += (f'<div style="flex:1;min-width:240px;background:#0f2942;padding:1.25rem;border-radius:12px;border-left:4px solid {v["cor"]};">'
                  f'<div style="color:#94a3b8;font-size:.9rem;">{canal}</div>'
                  f'<div style="font-size:2rem;color:#fff;">{v["total"]}</div><div style="color:#94a3b8;">leads</div>'
                  f'<div style="margin-top:.6rem;color:{v["cor"]};">↳ {v["resp"]} responderam ({v["tx_resp"]:.1f}%)</div>'
                  f'<div style="color:#4ade80;">↳ {v["fechou"]} fechados ({v["tx_fech"]:.1f}%)</div>'
                  f'<div style="color:#facc15;">↳ R$ {v["valor"]:,.0f}</div></div>')

    html = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Outbound Proprietários — Praia Digital</title></head><body style="margin:0;font-family:Segoe UI,Arial,sans-serif;background:#07111f;color:#e2e8f0;"><div style="max-width:1000px;margin:0 auto;padding:2rem;"><h1 style="color:#fff;">🌊 Outbound — Proprietários Autogestores</h1><p style="color:#94a3b8;">Consolidado WhatsApp + E-mail · {date.today():%d/%m/%Y} · Praia Digital</p><div style="display:flex;gap:1rem;flex-wrap:wrap;margin:1.5rem 0;"><div style="flex:1;min-width:200px;background:#0f2942;padding:1.25rem;border-radius:12px;"><div style="font-size:2rem;color:#fff;">{tot_leads}</div><div style="color:#94a3b8;">Leads totais (2 canais)</div></div><div style="flex:1;min-width:200px;background:#0f2942;padding:1.25rem;border-radius:12px;"><div style="font-size:2rem;color:#4ade80;">{tot_fech}</div><div style="color:#94a3b8;">Fechados (soma)</div></div><div style="flex:1;min-width:200px;background:#0f2942;padding:1.25rem;border-radius:12px;"><div style="font-size:2rem;color:#facc15;">R$ {tot_valor:,.0f}</div><div style="color:#94a3b8;">Receita estimada</div></div></div><h2 style="color:#fff;">Por canal</h2><div style="display:flex;gap:1rem;flex-wrap:wrap;">{cards}</div><p style="color:#64748b;margin-top:2rem;font-size:.8rem;">Fontes: tracker-whatsapp-proprietarios.csv · tracker-email-proprietarios.csv</p></div></body></html>"""
    open(OUT, "w", encoding="utf-8").write(html)
    print(f"Dashboard consolidado: {OUT}\nLeads totais: {tot_leads} | Fechados: {tot_fech} | Receita R${tot_valor:,.0f}")

if __name__ == "__main__":
    main()
