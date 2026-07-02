#!/usr/bin/env python3
"""
Abre e-mails de prospecção B2B usando mailto em lote.
Uso:
  python scripts/outreach_mailto.py [--limit 5]
Gera arquivo outreach/outlook_batch.html e abre no navegador.
"""
import csv, urllib.parse, textwrap, webbrowser, os
from pathlib import Path

LEADS_CSV = Path(__file__).resolve().parents[1] / "docs/sales/leads-litoral-enriquecido.csv"
OUT_DIR = Path(__file__).resolve().parents[1] / "outreach"
OUT_DIR.mkdir(exist_ok=True)

BASE = """Assunto: Parceria B2B em IA — {t} para {e}

Prezado(a) {c},

Escrevo como CEO da Praia Digital para propor uma colaboração direta para a {e} em {city}.

Somos a primeira plataforma do litoral paulista com IA aplicada a imóveis de praia. Hoje ajudamos empresas do setor a captar leads qualificados e fechar mais negócios, sem alterar o site atual.

Serviços em destaque:
• {b1}
• {b2}
• {b3}

Ferramentas gratuitas para validação prévia: https://praia.digital

Se fizer sentido, proponho uma demonstração de 20 minutos.

Atenciosamente,
Carolina Mourad
CEO — Praia Digital
(11) 95434-6288 | comercial@praia.digital
https://praia.digital"""

diff = {
  'chatbot': ('Chatbot 24h no site','Atendimento automático 24/7 com qualificação de leads e encaminhamento para WhatsApp.','Integração sem alterar layout atual.'),
  'avaliacao': ('Avaliação automática de imóvel','Relatórios com scoring de oportunidade e preço justo por bairro.','PDF profissional para compartilhar com clientes.'),
  'seo': ('SEO local + conteúdo IA','10 artigos/mês otimizados para cidade/bairro, atraindo tráfego qualificado.','Mais visitas orgânicas com alta intenção de compra.'),
  'relatorios': ('Relatórios mensais de mercado','Valorização por bairro, sazonalidade e tempo médio de venda/locação.','PDF enviado todo mês para você compartilhar com clientes.'),
  'anuncios': ('Anúncios com IA para temporada e portais','Descrições profissionais, sugestão de fotos e precificação dinâmica.','Aumento de CTR e redução de custo por lead.')
}

with open(LEADS_CSV, 'r', encoding='utf-8') as f:
    leads = list(csv.DictReader(f))

import argparse
ap = argparse.ArgumentParser()
ap.add_argument('--limit', type=int, default=50)
args = ap.parse_args()
leads = leads[:args.limit]

items = []
for i, r in enumerate(leads, 1):
    dk = r.get('diferencial', 'chatbot')
    t = diff.get(dk, diff['chatbot'])
    corpo = BASE.format(t=t[0], e=r.get('nome_da_imobiliaria', 'sua operação'), city=r.get('cidade', 'o litoral paulista'), c=r.get('pessoa_de_contato', 'Responsável'), b1=t[0], b2=t[1], b3=t[2])
    subj = f"Parceria B2B em IA — {t[0]} para {r.get('nome_da_imobiliaria', '')}"
    mailto = f"mailto:{r.get('email', '')}?{urllib.parse.urlencode({'subject': subj, 'body': corpo})}"
    items.append((i, r.get('nome_da_imobiliaria', ''), r.get('cidade', ''), r.get('email', ''), mailto))

html = f"""<!DOCTYPE html><html lang='pt-BR'><head><meta charset='UTF-8'><title>Outreach B2B</title><style>
body{{font-family:Segoe UI,system-ui,sans-serif;background:#F4EBD0;color:#023047;margin:0;padding:2rem;}}
table{{border-collapse:collapse;width:100%;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,0.06);}}
th,td{{padding:0.85rem 1rem;border-bottom:1px solid #f1f5f9;text-align:left;font-size:0.95rem;}}
th{{background:#0077B6;color:#fff;}}
a{{display:inline-block;background:#0077B6;color:#fff;padding:.45rem .9rem;border-radius:999px;text-decoration:none;font-weight:700;}}
</style></head><body><h1>Outreach B2B — clique para abrir cada e-mail</h1>
<table><thead><tr><th>#</th><th>Imobiliária</th><th>Cidade</th><th>E-mail</th><th>Ação</th></tr></thead><tbody>
{''.join(f'<tr><td>{i}</td><td>{n}</td><td>{c}</td><td>{e}</td><td><a href="{m}" target="_blank">Abrir e-mail</a></td></tr>' for i,n,c,e,m in items)}
</tbody></table></body></html>"""

out_path = OUT_DIR / 'outlook_batch.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)
print('Gerado:', out_path, 'com', len(items), 'e-mails')
webbrowser.open(f'file:///{out_path.as_posix()}')
