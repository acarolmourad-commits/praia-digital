import json
from pathlib import Path
from datetime import date

base = Path('C:/Users/Carolina/praia-digital/litoral-prime-imoveis')
properties = json.loads((base / 'imoveis' / 'properties.json').read_text(encoding='utf-8'))
today = date.today().isoformat()

by_city = {}
for p in properties:
    by_city.setdefault(p['city'], []).append(p)

marketing_dir = base / 'marketing'
marketing_dir.mkdir(parents=True, exist_ok=True)

for city, items in by_city.items():
    top = sorted(items, key=lambda x: x['score'], reverse=True)[:3]
    best = top[0]
    city_lower = city.lower()
    
    wa_lines = [
        f'# Copy WhatsApp — {city}',
        '',
        '## Lista curta',
        f'1. "Olá! Encontrei opções exclusivas em {city}. Quer ver as 3 melhores oportunidades desta semana?"',
        f'2. "Tenho imóveis em {city} com condições facilitadas. Qual perfil: compra, aluguel ou temporada?"',
        f'3. "Esta unidade em {best["title"]} está com alta procura. Quero garantir seu atendimento prioritário."',
        f'4. "Selecionamos imóveis em {city} para você. Deseja receber as opções por WhatsApp?"',
        f'5. "Atendimento especializado em {city}. Qual o melhor horário para enviar as opções?"',
        ''
    ]
    (marketing_dir / f'{city_lower}-whatsapp.md').write_text('\n'.join(wa_lines), encoding='utf-8')
    
    email_subjects = [
        f'Oportunidades em {city} — Litoral Prime Imóveis',
        f'3 imóveis selecionados para você em {city}',
        f'Acesso antecipado: imóveis em {city} com condições especiais'
    ]
    
    email_lines = ['# E-mail — ' + city, '', '## Assuntos']
    for i, s in enumerate(email_subjects):
        email_lines.append(f'{i+1}. {s}')
    email_lines += ['', '## Corpos']
    top_titles = '\n'.join([f'- {p["title"]}: {p["price"]} — {p["area"]}' for p in top])
    top_titles_simple = '\n'.join([f'- {p["title"]}: {p["price"]}' for p in top])
    bodies = [
        f"Olá,\n\nTemos oportunidades exclusivas em {city}.\n\nDestaques:\n{top_titles}\n\nResponda este e-mail ou chame no WhatsApp: (11) 95434-6288",
        f"Olá,\n\nSelecionamos imóveis em {city} para o seu perfil.\n\n{top_titles_simple}\n\nQuer ver mais? Clique no botão do WhatsApp.",
        f"Olá,\n\nAcesso antecipado para imóveis em {city}.\n\n{top_titles_simple}\n\nGaranta sua preferência no atendimento."
    ]
    for i, b in enumerate(bodies):
        email_lines.append(f'### E-mail {i+1}\n{b}')
    
    (marketing_dir / f'{city_lower}-email.md').write_text('\n'.join(email_lines), encoding='utf-8')
    
    campaign = f"""# Campanha rápida — {city}
Público: proprietários, investidores e corretores no litoral.
Objetivo: agendar atendimento no WhatsApp.
Formato: copy + link direto + CTA claro.
"""
    (marketing_dir / f'{city_lower}-campanha.md').write_text(campaign, encoding='utf-8')

kit = """# Kit de Crescimento Rápido — Litoral Prime Imóveis
## Objetivo
Aumentar atendimentos qualificados no WhatsApp e gerar mais visitas/imóveis fechados.

## Ações rápidas
1. Publicar 1 post por cidade com destaque de imóvel e CTA WhatsApp.
2. Enviar 5 mensagens por dia usando as copias por cidade.
3. Atualizar status do atendimento nas páginas de cidade.

## Métricas
- Atendimentos iniciados no WhatsApp
- Respostas por cidade
- Leads qualificados por semana
"""
(marketing_dir / 'crescimento-rapido.md').write_text(kit, encoding='utf-8')

print('Ativos de conversão criados em', marketing_dir)
