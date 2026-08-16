# Auditoria de vazamentos de valor — 2026-08-16
import re
from pathlib import Path

root=Path('C:/Users/Carolina/praia-digital')
out=root/'docs'/'comercial'/'auditoria_vazamentos_valor_2026-08-16.md'

# Escopo reduzido para arquivos específicos para evitar timeout
files=list((root/'blog').glob('*.html'))[:50]
report=[]
without_cta=[]
cta_no_dest=[]
services_without_content=[]
content_without_service=[]
courses_without_acquisition=[]
traffic_poor_monetization=[]

services=['administração airbnb','administracao airbnb','edição de anúncio','edicao de anuncio','fotografia','seo local','administração temporada','administracao temporada']
academy_keywords=['academy','curso','aula']
cta_patterns=re.compile(r'class="[^"]*cta|cta|compre|matricule|contrat', re.I)

for path in files:
    text=path.read_text(encoding='utf-8', errors='ignore')
    has_cta=bool(cta_patterns.search(text))
    title=re.search(r'<title[^>]*>(.*?)</title>', text, re.I)
    title_text=title.group(1) if title else path.name
    if not has_cta:
        without_cta.append(path.name)
    lower=text.lower()
    svc_found=[s for s in services if s in lower]
    aca_found=[a for a in academy_keywords if a in lower]
    if svc_found and not aca_found:
        content_without_service.append((path.name, svc_found))
    if not svc_found and aca_found:
        services_without_content.append(path.name)
    if not has_cta and ('invest' in lower or 'temporada' in lower or 'aluguel' in lower):
        traffic_poor_monetization.append(path.name)

lines=['# Auditoria de vazamentos de valor — 2026-08-16\n','Escopo: 50 páginas do blog para varredura inicial.\n']
lines.append(f'- Páginas sem CTA: {len(without_cta)}')
lines.append(f'- Conteúdo comercial sem serviço/curso correspondente: {len(content_without_service)}')
lines.append(f'- Conteúdo sem serviço/curso correspondente: {len(services_without_content)}')
lines.append(f'- Páginas com potencial de tráfego mas baixa monetização: {len(traffic_poor_monetization)}')
lines.append('\n## Amostras — conteúdo sem CTA\n')
for x in without_cta[:15]:
    lines.append(f'- {x}')
lines.append('\n## Amostras — conteúdo com serviço mas sem CTA/curso\n')
for name, svc in content_without_service[:15]:
    lines.append(f'- {name}: {svc}')
lines.append('\n## Amostras — potencial tráfego sem monetização\n')
for x in traffic_poor_monetization[:15]:
    lines.append(f'- {x}')

out.write_text('\n'.join(lines), encoding='utf-8')
print(f'auditoria_vazamentos_valor_2026-08-16.md criada')
