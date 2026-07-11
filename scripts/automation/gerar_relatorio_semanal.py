#!/usr/bin/env python3
"""Gera relatório semanal automático em HTML consolidando conteúdo, envios e leads."""
from pathlib import Path
from datetime import datetime

BASE = Path(r'C:\Users\Carolina\praia-digital')
hoje = datetime.now().strftime('%Y-%m-%d')
OUT = BASE / f'docs/sales/relatorio-semanal-executivo-praia-digital-{hoje}.html'

TRACKER = BASE / 'docs/sales/followup-registro.md'
RESPONDERS = BASE / 'docs/sales/respostas-leads.csv'
FOLLOWUP_SCRIPT = 'scripts/automation/followup_auto_gatilho_resposta.py'
PENDING_SCRIPT = 'scripts/automation/gerar_convite_demo_15min.py'
NEXT_ACTIONS = [
    'Enviar follow-ups de D3 para leads que contataram hoje',
    'Executar followup_auto_gatilho_resposta.py para leads com resposta',
    'Agendar demonstrações de 15min para respostas de interesse alto',
    'Rodar gerador de propostas por lead automaticamente',
    'Publicar relas de SEO semanal para acompanhar indexação no Google'
]


def count_files(pattern, path='.'):
    p = BASE / path
    if not p.exists():
        return 0
    if pattern.endswith('/'):
        return sum(1 for x in p.rglob('*') if x.is_file() and x.parent == p)
    return len(list(p.glob(pattern)))


def main():
    hoje = datetime.now().strftime('%Y-%m-%d')
    blog_count = count_files('*.html', 'blog')
    imoveis_count = count_files('*.html', 'imoveis')
    docs_count = count_files('*.md', 'docs/materiais')
    outreach_count = count_files('*.html', 'outreach')

    tracker_lines = 0
    responder_count = 0
    if TRACKER.exists():
        tracker_lines = sum(1 for line in TRACKER.read_text(encoding='utf-8').splitlines() if line.strip().startswith('|') and 'Nome' not in line)
    if RESPONDERS.exists():
        responder_count = max(0, sum(1 for line in RESPONDERS.read_text(encoding='utf-8').splitlines()[1:] if line.strip() and not line.startswith('#') ) - 0)

    next_list = ''.join([f'<li>{a}</li>' for a in NEXT_ACTIONS])

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Relatório Semanal Executivo — Praia Digital — {hoje}</title>
  <style>
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:'Segoe UI',system-ui,sans-serif;background:#F4EBD0;color:#023047;line-height:1.7;padding:2rem}}
    .container{{max-width:1100px;margin:0 auto}}
    .hero{{background:linear-gradient(135deg,#0077B6,#00B4D8);color:#fff;padding:2rem;border-radius:18px;margin-bottom:1.5rem;text-align:center}}
    .hero h1{{font-size:clamp(1.6rem,4vw,2.4rem);margin-bottom:.5rem}}
    .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1rem;margin:1rem 0}}
    .card{{background:#fff;border-radius:14px;padding:1.2rem;box-shadow:0 2px 12px rgba(0,0,0,.08);text-align:center}}
    .metric{{font-size:1.8rem;font-weight:800;color:#0077B6;margin:.3rem 0}}
    .card h2{{font-size:1rem;color:#555;margin-top:.4rem}}
    .section{{background:#fff;border-radius:14px;padding:1.2rem;box-shadow:0 2px 12px rgba(0,0,0,.08);margin:1rem 0}}
    .section h2{{color:#0077B6;margin-bottom:.6rem}}
    .btn{{display:inline-block;background:#0077B6;color:#fff;padding:.6rem 1.1rem;border-radius:999px;text-decoration:none;font-weight:700;margin:.25rem}}
    .btn-green{{background:#25D366}}
    .btn-orange{{background:#F97316}}
    .small{{font-size:.9rem;color:#555}}
  </style>
</head>
<body>
  <div class="container">
    <div class="hero">
      <h1>Relatório Semanal Executivo — Praia Digital</h1>
      <p>Data: {hoje} · Visão executiva de conteúdo, prospecção e indexação</p>
      <a class="btn btn-green" href="docs/sales/relatorio-diario-outbound-{hoje}.html" target="_blank">Relatório diário</a>
      <a class="btn" href="docs/sales/painel-diario-unificado-praia-digital-2026.html" target="_blank">Painel do dia</a>
    </div>

    <div class="grid">
      <div class="card">
        <div class="metric">{blog_count}</div>
        <h2>Artigos SEO</h2>
      </div>
      <div class="card">
        <div class="metric">{imoveis_count}</div>
        <h2>Imóveis cadastrados</h2>
      </div>
      <div class="card">
        <div class="metric">{docs_count}</div>
        <h2>Docs e materiais</h2>
      </div>
      <div class="card">
        <div class="metric">{outreach_count}</div>
        <h2>Ativos de outreach</h2>
      </div>
      <div class="card">
        <div class="metric">{tracker_lines}</div>
        <h2>Registros no tracker</h2>
      </div>
      <div class="card">
        <div class="metric">{responder_count}</div>
        <h2>Respostas pendentes</h2>
      </div>
    </div>

    <div class="section">
      <h2>Sumário executivo</h2>
      <p class="small">Base de conteúdo expandida: {blog_count} artigos SEO, {imoveis_count} imóveis e {docs_count} materiais. Operação comercial com {tracker_lines} registros e {responder_count} respostas pendentes.</p>
    </div>

    <div class="section">
      <h2>Execução e automação</h2>
      <p class="small">Rotinas prontas: follow-up por gatilho, relatório diário, checklist diária, lançador de sitemap e roteiros de vídeo automáticos.</p>
    </div>

    <div class="section">
      <h2>Próximas ações</h2>
      <ul>
        {next_list}
      </ul>
    </div>

    <div class="small" style="text-align:center">
      Site oficial: https://acarolmourad-commits.github.io/praia-digital/ · Ferramentas: https://praia.digital
    </div>
  </div>
</body>
</html>"""

    OUT.write_text(html, encoding='utf-8')
    print(f'GERADO: {OUT}')



if __name__ == '__main__':
    main()
