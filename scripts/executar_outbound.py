#!/usr/bin/env python3
"""Orquestrador mestre do outbound proprietarios autogestores.
Consolida trackers WPP+email, gera os 3 dashboards (com metas) e opcionalmente
faz commit+push dos artefatos atualizados.

Uso:
  python scripts/executar_outbound.py            # so consolida+dashboards
  python scripts/executar_outbound.py --push     # + git commit/push
"""
import argparse, csv, os, json, subprocess
from collections import defaultdict
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
DIR = os.path.join(REPO, "docs/sales/csv-lotes-email")
OUT = os.path.join(REPO, "docs/sales", "dashboard-outbound-proprietarios.html")
METAS = os.path.join(REPO, "docs/sales", "METAS_OUTBOUND.json")

CANAIS = {
    "WhatsApp": {"tracker": os.path.join(DIR, "tracker-whatsapp-proprietarios.csv"), "cor": "#22d3ee"},
    "E-mail":   {"tracker": os.path.join(DIR, "tracker-email-proprietarios.csv"), "cor": "#a78bfa"},
}

def ler(tracker):
    if not os.path.exists(tracker): return []
    return list(csv.DictReader(open(tracker, encoding="utf-8-sig"), delimiter=";"))

def run(py): subprocess.run(["python", os.path.join(REPO, "scripts", py)], check=True)

def bar(pct, cor):
    p = min(pct, 100)
    return (f'<div style="flex:1;background:#0f2942;border-radius:6px;overflow:hidden;height:14px;">'
            f'<div style="width:{p:.1f}%;background:{cor};height:14px;"></div></div>')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--push", action="store_true", help="faz git commit/push dos artefatos")
    args = ap.parse_args()
    # 1) consolidar + dashboards por canal
    run("consolidar_tracker_whatsapp.py"); run("gerar_dashboard_whatsapp.py")
    run("consolidar_tracker_email.py");    run("gerar_dashboard_email.py")

    # 2b) prova de entrega (auditoria)
    run("gerar_prova_entrega.py")
    # 2c) relatorio de acoes de conversao (respondeu -> Msg2.5, fechou -> Msg4)
    run("relatorio_acoes_conversao.py")
    # 2d) relatorio de nurture/win-back (sem_interesse em D+30/60/90)
    run("relatorio_nurture.py")

    # 3) consolidado com metas
    res = {}
    for canal, cfg in CANAIS.items():
        rows = ler(cfg["tracker"]); cnt = defaultdict(int)
        for r in rows: cnt[r["Status"]] += 1
        resp = cnt["respondeu"] + cnt["fechou"]; fechou = cnt["fechou"]
        sem = cnt.get("sem_interesse", 0); ativos = len(rows) - sem
        valor = sum(float(r["Valor_Estimado"]) for r in rows if r.get("Valor_Estimado"))
        res[canal] = dict(total=len(rows), resp=resp, fechou=fechou, valor=valor,
                          tx_resp=(resp/ativos*100) if ativos else 0,
                          tx_fech=(fechou/ativos*100) if ativos else 0, cor=cfg["cor"])
    tot_leads = sum(v["total"] for v in res.values())
    tot_fech = sum(v["fechou"] for v in res.values())
    tot_valor = sum(v["valor"] for v in res.values())
    tot_resp = sum(v["resp"] for v in res.values())

    metas = json.load(open(METAS, encoding="utf-8"))["metas"]
    def meta_row(label, atual, meta, cor):
        pct = (atual/meta*100) if meta else 0
        return (f'<div style="margin:.5rem 0;"><div style="display:flex;justify-content:space-between;color:#cbd5e1;font-size:.9rem;">'
                f'<span>{label}</span><span>{atual} / {meta} ({pct:.0f}%)</span></div>{bar(pct, cor)}</div>')
    metas_html = (f'<div style="background:#0f2942;padding:1.25rem;border-radius:12px;margin:1.5rem 0;">'
                  f'<h2 style="color:#fff;margin-bottom:.6rem;">🎯 Metas {date.today():%m/%Y}</h2>'
                  + meta_row("Responderam", tot_resp, metas["respondeu"], "#22d3ee")
                  + meta_row("Fechados", tot_fech, metas["fechou"], "#4ade80")
                  + meta_row("Receita estimada (R$)", int(tot_valor), metas["receita_estimada"], "#facc15")
                  + '</div>')

    cards = ""
    for canal, v in res.items():
        cards += (f'<div style="flex:1;min-width:240px;background:#0f2942;padding:1.25rem;border-radius:12px;border-left:4px solid {v["cor"]};">'
                  f'<div style="color:#94a3b8;font-size:.9rem;">{canal}</div>'
                  f'<div style="font-size:2rem;color:#fff;">{v["total"]}</div><div style="color:#94a3b8;">leads</div>'
                  f'<div style="margin-top:.6rem;color:{v["cor"]};">↳ {v["resp"]} responderam ({v["tx_resp"]:.1f}%)</div>'
                  f'<div style="color:#4ade80;">↳ {v["fechou"]} fechados ({v["tx_fech"]:.1f}%)</div>'
                  f'<div style="color:#facc15;">↳ R$ {v["valor"]:,.0f}</div></div>')

    html = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Outbound Proprietários — Praia Digital</title></head><body style="margin:0;font-family:Segoe UI,Arial,sans-serif;background:#07111f;color:#e2e8f0;"><div style="max-width:1000px;margin:0 auto;padding:2rem;"><h1 style="color:#fff;">🌊 Outbound — Proprietários Autogestores</h1><p style="color:#94a3b8;">Consolidado WhatsApp + E-mail · {date.today():%d/%m/%Y} · Praia Digital</p><div style="display:flex;gap:1rem;flex-wrap:wrap;margin:1.5rem 0;"><div style="flex:1;min-width:200px;background:#0f2942;padding:1.25rem;border-radius:12px;"><div style="font-size:2rem;color:#fff;">{tot_leads}</div><div style="color:#94a3b8;">Leads totais (2 canais)</div></div><div style="flex:1;min-width:200px;background:#0f2942;padding:1.25rem;border-radius:12px;"><div style="font-size:2rem;color:#4ade80;">{tot_fech}</div><div style="color:#94a3b8;">Fechados (soma)</div></div><div style="flex:1;min-width:200px;background:#0f2942;padding:1.25rem;border-radius:12px;"><div style="font-size:2rem;color:#facc15;">R$ {tot_valor:,.0f}</div><div style="color:#94a3b8;">Receita estimada</div></div></div>{metas_html}<h2 style="color:#fff;">Por canal</h2><div style="display:flex;gap:1rem;flex-wrap:wrap;">{cards}</div><p style="color:#64748b;margin-top:2rem;font-size:.8rem;">Fontes: tracker-whatsapp-proprietarios.csv · tracker-email-proprietarios.csv · METAS_OUTBOUND.json</p></div></body></html>"""
    open(OUT, "w", encoding="utf-8").write(html)
    print(f"Dashboard consolidado: {OUT}\nLeads {tot_leads} | Resp {tot_resp} | Fech {tot_fech} | R${tot_valor:,.0f}")

    # 3) commit+push opcional
    if args.push:
        subprocess.run(["git", "-C", REPO, "add", "docs/sales/csv-lotes-email/tracker-whatsapp-proprietarios.csv",
                        "docs/sales/csv-lotes-email/tracker-email-proprietarios.csv", "docs/sales/dashboard-whatsapp-proprietarios.html",
                        "docs/sales/dashboard-email-proprietarios.html", "docs/sales/dashboard-outbound-proprietarios.html",
                        "docs/sales/prova-entrega-outbound.json", "docs/sales/prova-entrega-outbound.html"], check=True)
        subprocess.run(["git", "-C", REPO, "commit", "-m", f"chore: refresh dashboards outbound {date.today():%Y-%m-%d}"], check=True)
        subprocess.run(["git", "-C", REPO, "push"], check=True)
        print("Commit+push dos artefatos atualizados.")

if __name__ == "__main__":
    main()
