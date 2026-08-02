#!/usr/bin/env python3
"""
add_service_schema.py
Adiciona Service JSON-LD nas páginas de serviço que ainda não têm esse schema.
"""
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

service_map = {
    'servico-complementar-assinatura-digital-imoveis-2026.html': 'Assinatura Digital para Imóveis',
    'servico-complementar-avaliacao-preco-imoveis-ia-2026.html': 'Avaliação de Preço de Imóveis com IA',
    'servico-complementar-consultoria-proptech-2026.html': 'Consultoria Proptech',
    'servico-complementar-crm-imobiliario-2026.html': 'CRM Imobiliário',
    'servico-complementar-fotografia-tour-virtual-2026.html': 'Fotografia e Tour Virtual',
    'servico-complementar-gestao-anuncios-imobiliarios-2026.html': 'Gestão de Anúncios Imobiliários',
    'servico-complementar-gestao-locacao-imoveis-2026.html': 'Gestão de Locação de Imóveis',
    'servico-complementar-inspecao-laudo-tecnico-2026.html': 'Inspeção e Laudo Técnico',
    'servico-complementar-integracao-portais-2026.html': 'Integração com Portais',
    'servico-complementar-prospeccao-360-2026.html': 'Prospecção 360',
    'servico-fotografia-edicao.html': 'Fotografia e Edição',
    'captura-rapida.html': 'Captura Rápida',
    'checklist-leads.html': 'Checklist de Leads',
    'guia-aluguel-temporada.html': 'Guia de Aluguel por Temporada',
    'quero-vender-imovel-litoral.html': 'Venda de Imóvel no Litoral',
}

template = '''
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "{name}",
  "provider": {{
    "@type": "RealEstateAgent",
    "name": "Praia Digital"
  }},
  "areaServed": [
    "Santos","Guarujá","Praia Grande","Bertioga","Itanhaém","Mongaguá","São Vicente","Peruíbe"
  ],
  "availableLanguage": ["pt-BR","en"],
  "description": "Atendimento especializado para {name} no litoral de São Paulo."
}}
</script>
'''

updated = 0
skipped = 0
errors = 0
for path in sorted(BASE.rglob('*.html')):
    rel = path.relative_to(BASE)
    name = path.name
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        errors += 1
        continue
    if 'Service' in text:
        skipped += 1
        continue
    service_name = service_map.get(name)
    if not service_name:
        skipped += 1
        continue
    block = template.format(name=service_name)
    if '<head>' not in text:
        skipped += 1
        continue
    text = text.replace('<head>', '<head>\n' + block, 1)
    path.write_text(text, encoding='utf-8')
    print('updated', rel)
    updated += 1
print('done', 'updated=', updated, 'skipped=', skipped, 'errors=', errors)
