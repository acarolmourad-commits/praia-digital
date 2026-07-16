#!/usr/bin/env python3
"""
Dashboard de Expansao - Praia Digital (A/B/C/D).
Consolida status das 4 frentes + worklist priorizada de B2B (Partner Score) num HTML.
Le os dados REAIS do repo. Uso: python scripts/gerar_dashboard_expansao.py
"""
import csv, os, glob, re
from collections import Counter
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
B2B = os.path.join(REPO, "docs/materiais/leads-litoral-enriquecido.csv")
REV = os.path.join(REPO, "docs/sales/csv-lotes-b2b/lote-b2b-reativacao-2026-07-16.csv")
WL = os.path.join(REPO, "docs/sales/csv-lotes-b2b/lote-b2b-whitelabel-2026-07-16.csv")
OUT = os.path.join(REPO, "docs/product/dashboard-expansao.html")

# dados reais
rows = list(csv.DictReader(open(B2B, encoding="utf-8-sig")))
fechadas = [r for r in rows if r["status"] == "parceria_fechada"]
pend = [r for r in rows if r["status"] == "contato_inicial_enviado"]
rev_n = len(list(csv.DictReader(open(REV, encoding="utf-8-sig"), delimiter=";"))) if os.path.exists(REV) else 0
wl_n = len(list(csv.DictReader(open(WL, encoding="utf-8-sig"), delimiter=";"))) if os.path.exists(WL) else 0
landings_n = len(glob.glob(os.path.join(REPO, "parcerias-norte", "*.html")))
dono_n = len(glob.glob(os.path.join(REPO, "dono-norte", "*.html")))
cta_n = sum(1 for f in glob.glob(os.path.join(REPO, "blog", "*.html"))
            if "CTA-PARCEIRA-PRAIA-DIGITAL-NORTE" in open(f, encoding="utf-8", errors="ignore").read()
            or "CTA-B2C-PRAIA-DIGITAL-NORTE" in open(f, encoding="utf-8", errors="ignore").read())

# worklist priorizada (Partner Score) - top 20 reativacao
def score(r):
    try: return float(r.get("_score") or 0)
    except: return 0
top = sorted(pend, key=score, reverse=True)[:20]

hoje = date.today().isoformat()
circulos = f"""
<div class="kpi">
<div class="card"><b>{len(rows)}</b><span>Leads B2B base</span></div>
<div class="card"><b>{len(fechadas)}</b><span>Parcerias fechadas</span></div>
<div class="card"><b>{rev_n+wl_n}</b><span>B2B armados p/ disparo</span></div>
<div class="card"><b>{landings_n+dono_n}</b><span>Landings norte (B2B+B2C)</span></div>
</div>"""

frentes = f"""
<table><tr class="th"><th>Frente</th><th>Público</th><th>Status</th><th>No ar?</th></tr>
<tr><td>A — B2B Imobiliárias</td><td>486 reativação + 101 white-label</td><td>CSV consolidado pronto</td><td class="pend">armada (aguarda disparo)</td></tr>
<tr><td>B — Norte B2B</td><td>Imobiliárias norte</td><td>{landings_n} landings + CTAs</td><td class="ok">ao vivo</td></tr>
<tr><td>C — White-label Calc</td><td>101 parceiras</td><td>widget + standalone</td><td class="ok">ao vivo</td></tr>
<tr><td>D — Norte B2C</td><td>Donos norte</td><td>{dono_n} landings + {cta_n} CTAs</td><td class="ok">ao vivo</td></tr>
</table>"""

worklist = "<table><tr class='th'><th>#</th><th>Imobiliária</th><th>Cidade</th><th>Score</th><th>Perfil</th></tr>"
for i, r in enumerate(top, 1):
    worklist += f"<tr><td>{i}</td><td>{r['nome_da_imobiliaria']}</td><td>{r['cidade']}</td><td>{r.get('_score')}</td><td>{r['perfil']}</td></tr>"
worklist += "</table>"

HTML = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard de Expansão — Praia Digital</title>
<style>body{{font-family:Arial,sans-serif;max-width:880px;margin:auto;padding:24px;color:#112}}
h1{{color:#0a3a6b}}h2{{color:#0a3a6b;border-bottom:2px solid #e2e8f0;padding-bottom:4px;margin-top:1.5rem}}
.card{{background:#f0f7ff;border:1px solid #cfe3f5;border-radius:10px;padding:12px;text-align:center}}
.card b{{font-size:1.5rem;color:#0a3a6b;display:block}}.card span{{font-size:.75rem;color:#667}}
.kpi{{display:flex;gap:10px;flex-wrap:wrap;margin:12px 0}}
table{{width:100%;border-collapse:collapse;margin:10px 0}}th,td{{border:1px solid #e2e8f0;padding:6px;text-align:left;font-size:.85rem}}
.ok{{color:#16a34a;font-weight:700}}.pend{{color:#d97706}}.th{{background:#f0f7ff}}
.banner{{background:#fffbeb;border:1px solid #fde68a;border-radius:10px;padding:12px;margin:12px 0;font-size:.9rem}}
li{{margin:4px 0}}</style></head><body>
<h1>🚀 Dashboard de Expansão — Praia Digital</h1>
<p>Gerado em {hoje} · dados reais do repo.</p>
{circulos}
<div class="banner">⚠️ <b>Próximo passo crítico:</b> disparar o B2B A ({rev_n+wl_n} imobiliárias) — basta rodar
<code>preparar_disparo_b2b.py</code> + <code>marcar_primeiro_envio_b2b.py</code>. Requer autorização (escala 3× o outbound).</div>
<h2>Frentes (A/B/C/D)</h2>
{frentes}
<h2>Worklist Priorizada — Top 20 B2B p/ reativação (Partner Score)</h2>
<p>Ordenado por <code>_score</code> (pontuação de lead da base). Disparar na ordem maximiza conversão.</p>
{worklist}
<h2>Próximos temas sugeridos</h2>
<ul>
<li>Calibrar calculadora (exportar contratos reais → <code>docs/data/reservas-internas.csv</code>)</li>
<li>Nova frente geográfica (Floripa / RJ) ou novo produto (seguro de temporada)</li>
<li>Inside-sales: nutrir os leads norte que já entram via SEO</li>
</ul>
<p style="font-size:.8rem;color:#667">Praia Digital · Estratégia de Expansão Produto/Mercado</p>
</body></html>"""

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"Dashboard de expansao: {OUT}")
print(f"  B2B={len(rows)} fechadas={len(fechadas)} pend={len(pend)} armados={rev_n+wl_n} landings_norte={landings_n+dono_n} CTAs_norte={cta_n}")
