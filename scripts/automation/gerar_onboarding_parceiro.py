
import csv, shutil
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital')
OUT = BASE / 'docs' / 'sales' / 'onboarding-parceiros'
CSV = BASE / 'docs' / 'sales' / 'leads-litoral-enriquecido-realista.csv'

# Limpa pasta antes de regenerar
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True, exist_ok=True)

if not CSV.exists():
    print('Base realista não encontrada.')
    raise SystemExit(0)

template_email = """Olá, {nome_contato}!

Obrigado pela parceria. Abaixo está o pacote do piloto sem custo por 14 dias:

1. Diagnóstico do funil: captação, atendimento e fechamento
2. Ferramentas gratuitas: https://praia.digital
3. Follow-up automático e tracking de leads
4. Relatório semanal de resultado

Próximo passo: responder este e-mail com melhor horário para uma demonstração de 15min.

Contato: comercial@praia.digital | WhatsApp: (11) 95434-6288
"""

template_whatsapp = """Olá, {nome_contato}! Tudo bem?

Sou da Praia Digital e preparei o pacote de piloto sem custo para {nome_imobiliaria}:

- Diagnóstico gratuito do funil
- Ferramentas de IA sem taxa de setup
- Follow-up automático e relatório semanal

Quer seguir com o diagnóstico esta semana?
"""

summary_template = """Empresa: {nome_imobiliaria}
Contato: {nome_contato}
Cidade: {cidade}
E-mail: {email}
WhatsApp: {whatsapp}
Piloto: 14 dias sem custo
Objetivo: captação + follow-up automático + relatório semanal
"""

with CSV.open('r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    empresas = set()
    count = 0
    for idx, row in enumerate(reader, start=1):
        nome_imobiliaria = row.get('nome_imobiliaria') or ''
        nome_contato = row.get('nome_contato') or ''
        cidade = row.get('cidade') or ''
        email = row.get('email') or ''
        whatsapp = row.get('whatsapp') or ''
        key = f"{nome_imobiliaria}-{cidade}".lower()
        if key in empresas:
            continue
        empresas.add(key)
        count += 1
        pasta = OUT / f"parceiro-{count:03d}-{nome_imobiliaria}-{cidade}"
        pasta.mkdir(parents=True, exist_ok=True)
        (pasta / 'email-boas-vindas.txt').write_text(
            template_email.format(nome_contato=nome_contato, nome_imobiliaria=nome_imobiliaria, cidade=cidade, email=email),
            encoding='utf-8'
        )
        (pasta / 'whatsapp-boas-vindas.txt').write_text(
            template_whatsapp.format(nome_contato=nome_contato, nome_imobiliaria=nome_imobiliaria, cidade=cidade, whatsapp=whatsapp),
            encoding='utf-8'
        )
        (pasta / 'resumo-parceiro.txt').write_text(
            summary_template.format(nome_imobiliaria=nome_imobiliaria, nome_contato=nome_contato, cidade=cidade, email=email, whatsapp=whatsapp),
            encoding='utf-8'
        )
        if count >= 5:
            break

print(f'Onboarding gerado para {count} parceiros únicos em {OUT}')
