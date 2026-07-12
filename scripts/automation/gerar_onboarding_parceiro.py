
import csv, datetime, os
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital')
OUT = BASE / 'docs' / 'sales' / 'onboarding-parceiros'
OUT.mkdir(parents=True, exist_ok=True)

template_email = """Olá, {nome}!

Obrigado pela parceria. Abaixo está o pacote do piloto sem custo por 14 dias:

1. Diagnóstico do funil: captação, atendimento e fechamento
2. Ferramentas gratuitas: https://praia.digital
3. Follow-up automático e tracking de leads
4. Relatório semanal de resultado

Próximo passo: responder este e-mail com melhor horário para uma demonstração de 15min.

Contato: comercial@praia.digital | WhatsApp: (11) 95434-6288
"""

template_whatsapp = """Olá, {nome}! Tudo bem?

Sou da Praia Digital e preparei o pacote de piloto sem custo para {empresa}:

- Diagnóstico gratuito do funil
- Ferramentas de IA sem taxa de setup
- Follow-up automático e relatório semanal

Quer seguir com o diagnóstico esta semana?
"""


def slug(s):
    return "".join(c if c.isalnum() or c == "-" else "" for c in s).strip()


def build_package(row, idx):
    nome = row.get('nome_contato') or row.get('NOME_CONTATO') or 'Parceiro'
    empresa = row.get('nome_imobiliaria') or row.get('NOME_IMOBILIARIA') or 'Imobiliária'
    cidade = row.get('cidade') or row.get('CIDADE') or 'Litoral'
    email = row.get('email') or row.get('EMAIL') or 'contato@empresa.com'
    whatsapp = row.get('whatsapp') or row.get('WHATSAPP') or ''

    pasta = OUT / f"parceiro-{idx:03d}-{slug(empresa)}-{slug(cidade)}"
    pasta.mkdir(parents=True, exist_ok=True)

    (pasta / 'email-boas-vindas.txt').write_text(
        template_email.format(nome=nome, empresa=empresa, cidade=cidade, email=email),
        encoding='utf-8'
    )
    (pasta / 'whatsapp-boas-vindas.txt').write_text(
        template_whatsapp.format(nome=nome, empresa=empresa, cidade=cidade, whatsapp=whatsapp),
        encoding='utf-8'
    )
    summary = f"""Empresa: {empresa}
Nome: {nome}
Cidade: {cidade}
E-mail: {email}
WhatsApp: {whatsapp}
Piloto: 14 dias sem custo
Objetivo: captação + follow-up automático + relatório semanal
"""
    (pasta / 'resumo-parceiro.txt').write_text(summary, encoding='utf-8')
    return pasta


def main():
    csv_path = BASE / 'docs' / 'sales' / 'leads-litoral-enriquecido-realista.csv'
    created = []
    if not csv_path.exists():
        print('Base realista não encontrada.')
        raise SystemExit(0)
    with csv_path.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for idx, row in enumerate(reader, start=1):
            if idx > 5:
                break
            build_package(row, idx)
            empresa = row.get('nome_imobiliaria') or row.get('NOME_IMOBILIARIA') or ''
            cidade = row.get('cidade') or row.get('CIDADE') or ''
            created.append(f"{empresa} ({cidade})")

    print(f"Pacotes criados: {len(created)}")
    for c in created:
        print(f"- {c}")
    print(f"Saída: {OUT}")


if __name__ == '__main__':
    main()
