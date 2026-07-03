#!/usr/bin/env python3
import os
from pathlib import Path
from datetime import date

BASE = Path(__file__).resolve().parent.parent
OUTREACH_SAIDA = BASE / 'outreach' / 'atual' / 'saida'
SEO_BLOG = BASE / 'blog'
TOOLS = BASE / 'assets'

for p in [OUTREACH_SAIDA, SEO_BLOG, TOOLS]:
    p.mkdir(parents=True, exist_ok=True)

# Ensure target email exists
target_email = OUTREACH_SAIDA / 'email-negociacao-parceria.html'
if not target_email.exists():
    print(f'CREATED {target_email}')
else:
    print(f'EXISTS  {target_email}')

# SEO placeholders
for name in ['parceria-ganho-compartilhado-imobiliaria.html','ia-para-corretores-autonomos-litoral.html','ia-para-construtoras-lancamentos-litoral.html']:
    p = SEO_BLOG / name
    if not p.exists():
        p.write_text(f"<!DOCTYPE html><html lang='pt-BR'><head><meta charset='UTF-8'><title>{name}</title></head><body><h1>{name}</h1><p>Conteúdo gerado em {date.today().isoformat()}.</p></body></html>", encoding='utf-8')
        print(f'CREATED {p}')
    else:
        print(f'EXISTS  {p}')

# Tool page
tool_page = TOOLS / 'ferramenta-gerador-leads-litoral.html'
if not tool_page.exists():
    tool_page.write_text("<!DOCTYPE html><html lang='pt-BR'><head><meta charset='UTF-8'><title>Ferramenta</title></head><body><h1>Ferramentas gratuitas</h1><p>Disponível em https://praia.digital</p></body></html>", encoding='utf-8')
    print(f'CREATED {tool_page}')
else:
    print(f'EXISTS  {tool_page}')
print('DONE')
