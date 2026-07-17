#!/usr/bin/env python3
"""
Expansao I — Ranking de Ativacao White-label (gamificacao B2B).
Ranqueia as 101 parceiras white-label por score de prioridade (do lote) e gera:
  - docs/product/ranking-whitelabel.html (leaderboard + guia de ativacao do widget)
Reuso os dados reais do lote-b2b-whitelabel (Score/Dor/Imobiliaria).
Uso: python scripts/gerar_ranking_whitelabel.py
"""
import csv, os, re
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
LOTE = os.path.join(REPO, "docs/sales/csv-lotes-b2b/lote-b2b-whitelabel-2026-07-16.csv")
OUT = os.path.join(REPO, "docs/product/ranking-whitelabel.html")

def score(r):
    m = re.search(r"Score:\s*([\d.]+)", r.get("Obs", ""))
    try: return float(m.group(1)) if m else 0
    except: return 0

def main():
    rows = list(csv.DictReader(open(LOTE, encoding="utf-8-sig"), delimiter=";"))
    for r in rows:
        r["_score"] = score(r)
    rows.sort(key=lambda r: r["_score"], reverse=True)
    top = rows[:15]
    hoje = date.today().isoformat()

    lin = ""
    for i, r in enumerate(top, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        lin += (f"<tr><td>{medal}</td><td>{r['Imobiliaria']}</td><td>{r['Cidade']}</td>"
                f"<td class='ok'>{r['_score']:.0f}</td><td style='font-size:.78rem;color:#667'>{r.get('Dor','')[:40]}</td></tr>")

    HTML = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ranking White-label — Praia Digital</title>
<style>body{{font-family:Arial,sans-serif;max-width:820px;margin:auto;padding:24px;color:#112}}
h1{{color:#0a3a6b}}h2{{color:#0a3a6b;border-bottom:2px solid #e2e8f0;padding-bottom:4px;margin-top:1.5rem}}
.card{{background:linear-gradient(135deg,#1e3a8a,#0a3a6b);color:#fff;border-radius:12px;padding:1.2rem;margin:1rem 0}}
.card b{{font-size:2rem;display:block}}.card span{{opacity:.85}}
table{{width:100%;border-collapse:collapse;margin:10px 0}}th,td{{border:1px solid #e2e8f0;padding:8px;text-align:left;font-size:.85rem}}
.ok{{color:#16a34a;font-weight:700}}.th{{background:#f0f7ff}}
.guia{{background:#f0f7ff;border:1px solid #cfe3f5;border-radius:12px;padding:1.2rem;margin:1rem 0;line-height:1.7}}
code{{background:#e0f2fe;padding:2px 6px;border-radius:4px;font-size:.85rem}}
li{{margin:6px 0}}</style></head><body>
<h1>🏆 Ranking de Ativação White-label — Praia Digital</h1>
<p>Gerado em {hoje} · {len(rows)} parceiras white-label ranqueadas por prioridade.</p>
<div class="card"><b>{len(rows)}</b><span>parceiras prontas p/ ativar a Calculadora no próprio site</span></div>
<h2>Top 15 (prioridade de ativação)</h2>
<table><tr class='th'><th>#</th><th>Imobiliária</th><th>Cidade</th><th>Score</th><th>Sinal</th></tr>
{lin}</table>
<h2>Como ativar o widget no site da parceira (2 minutos)</h2>
<div class="guia">
<ol>
<li><b>Escolha a marca:</b> cada parceira tem um <code>tenant</code> (ex: <code>santos-ancora</code>).</li>
<li><b>Cole o iframe</b> na página de imóveis da parceira:
  <br><code>&lt;iframe src="https://praia.digital/assets/calculadora-widget-standalone.html?tenant=SEU-TENANT" width="100%" height="680"&gt;&lt;/iframe&gt;</code></li>
<li><b>Lead 100% da imobiliária:</b> todo dono que simula vira lead no <code>tracker-whitelabel.csv</code> com <code>parceiro_id</code>.</li>
<li><b>Revenue share 70/30:</b> quando fechamos a gestão, 70% da comissão é da parceira.</li>
<li><b>Suporte Praia Digital:</b> ajustamos a cor/marca e validamos o CEP da região.</li>
</ol>
</div>
<h2>Próximo passo</h2>
<p>Disparar as 101 propostas WL (já armadas em <code>lote-b2b-whitelabel-2026-07-16.csv</code>) e acompanhar a ativação no tracker. Quanto mais widgets ativos, mais inventário de gestão pro portfólio de cada parceira.</p>
<p style="font-size:.8rem;color:#667">Praia Digital · Expansão I — Gamificação White-label</p>
</body></html>"""
    open(OUT, "w", encoding="utf-8").write(HTML)
    print(f"Ranking white-label: {OUT}\n{len(rows)} parceiras ranqueadas | Top1: {top[0]['Imobiliaria']} ({top[0]['Cidade']}) score {top[0]['_score']:.0f}")

if __name__ == "__main__":
    main()
