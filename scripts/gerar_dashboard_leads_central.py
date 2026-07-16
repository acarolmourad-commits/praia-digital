#!/usr/bin/env python3
"""
Central Unificada de Leads (Expansao G) — le todos os trackers reais e gera 1 dashboard.
Consolida B2C (WPP+email), B2B (WPP+email), White-label numa visao unica de volume/status.
Uso: python scripts/gerar_dashboard_leads_central.py
"""
import csv, os, glob
from collections import Counter
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
CANAIS = [
    ("B2C WhatsApp", os.path.join(REPO, "docs/sales/csv-lotes-email/tracker-whatsapp-proprietarios.csv"), "whatsapp"),
    ("B2C E-mail", os.path.join(REPO, "docs/sales/csv-lotes-email/tracker-email-proprietarios.csv"), "email"),
    ("B2B WhatsApp", os.path.join(REPO, "docs/sales/csv-lotes-b2b/tracker-b2b.csv"), "whatsapp"),
    ("B2B E-mail", os.path.join(REPO, "docs/sales/csv-lotes-b2b/tracker-email-b2b.csv"), "email"),
    ("White-label", os.path.join(REPO, "docs/sales/csv-lotes-b2b/tracker-whitelabel.csv"), "whatsapp"),
]

def contar(p):
    if not os.path.exists(p): return 0, Counter()
    c = Counter()
    with open(p, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f, delimiter=";"):
            c[r.get("Status", "sem_status")] += 1
    return sum(c.values()), c

def main():
    lin = []
    tot = 0
    por_status = Counter()
    for nome, p, tipo in CANAIS:
        n, c = contar(p)
        tot += n
        por_status.update(c)
        fech = c.get("fechado", 0) + c.get("convertido", 0)
        lin.append((nome, tipo, n, fech, dict(c)))
    hoje = date.today().isoformat()

    cards = "".join(
        f'<div class="card"><b>{n}</b><span>{nome}<br>({tipo})</span><i>{fech} fechados</i></div>'
        for nome, tipo, n, fech, _ in lin)

    tabela = "<table><tr class='th'><th>Canal</th><th>Total</th><th>Fechados</th><th>Status detalhado</th></tr>"
    for nome, tipo, n, fech, c in lin:
        det = " · ".join(f"{k}:{v}" for k, v in sorted(c.items(), key=lambda x: -x[1]))
        tabela += f"<tr><td>{nome}</td><td>{n}</td><td class='ok'>{fech}</td><td style='font-size:.75rem;color:#667'>{det}</td></tr>"
    tabela += "</table>"

    resumo_status = " · ".join(f"{k}:{v}" for k, v in sorted(por_status.items(), key=lambda x: -x[1]))

    HTML = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Central de Leads — Praia Digital</title>
<style>body{{font-family:Arial,sans-serif;max-width:900px;margin:auto;padding:24px;color:#112}}
h1{{color:#0a3a6b}}h2{{color:#0a3a6b;border-bottom:2px solid #e2e8f0;padding-bottom:4px;margin-top:1.5rem}}
.card{{background:#f0f7ff;border:1px solid #cfe3f5;border-radius:10px;padding:12px;text-align:center;min-width:120px}}
.card b{{font-size:1.6rem;color:#0a3a6b;display:block}}.card span{{font-size:.78rem;color:#445;display:block}}
.card i{{font-size:.72rem;color:#16a34a;font-style:normal}}
.kpi{{display:flex;gap:10px;flex-wrap:wrap;margin:12px 0}}
table{{width:100%;border-collapse:collapse;margin:10px 0}}th,td{{border:1px solid #e2e8f0;padding:6px;text-align:left;font-size:.85rem}}
.ok{{color:#16a34a;font-weight:700}}.th{{background:#f0f7ff}}
.banner{{background:#fffbeb;border:1px solid #fde68a;border-radius:10px;padding:12px;margin:12px 0;font-size:.9rem}}
li{{margin:4px 0}}</style></head><body>
<h1>🎯 Central Unificada de Leads — Praia Digital</h1>
<p>Gerado em {hoje} · consolida {len(CANAIS)} trackers reais.</p>
<div class="kpi">{cards}</div>
<div class="banner">📊 <b>Total de leads nos trackers: {tot}</b><br>Status agregado: {resumo_status}</div>
<h2>Por canal</h2>
{tabela}
<h2>Próximas ações operacionais</h2>
<ul>
<li><b>Disparar B2B</b> (587 armados): <code>preparar_disparo_b2b.py</code> + <code>marcar_primeiro_envio_b2b.py</code> (WPP) e <code>consolidar_tracker_email_b2b.py</code> + <code>marcar_primeiro_envio_email_b2b.py</code> (e-mail)</li>
<li><b>Calibrar calculadora</b>: exportar contratos reais → <code>docs/data/reservas-internas.csv</code> → <code>ingest_historico_interno.py</code></li>
<li><b>Acompanhar</b>: crons diários avisam follow-ups (WPP 18h, e-mail 18h30, B2B 18h)</li>
</ul>
<p style="font-size:.8rem;color:#667">Praia Digital · Central de Leads (Expansão G)</p>
</body></html>"""
    OUT = os.path.join(REPO, "docs/sales/central-leads.html")
    open(OUT, "w", encoding="utf-8").write(HTML)
    print(f"Central de Leads: {OUT}\nTotal leads: {tot} | canais: {len(CANAIS)}")

if __name__ == "__main__":
    main()
