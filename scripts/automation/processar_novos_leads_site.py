
import csv, os, datetime
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital')
LEADS_CSV = BASE / 'docs' / 'sales' / 'parcerias-leads-capturados.csv'
OUT_CSV = BASE / 'docs' / 'sales' / 'novos-leads-site-2026-07-12.csv'
TRACKER = BASE / 'docs' / 'sales' / 'followup-registro.md'

OUT_DIR = BASE / 'outreach' / 'followups-pendentes'
OUT_DIR.mkdir(parents=True, exist_ok=True)

hoje = datetime.datetime.now().strftime('%Y-%m-%d')
consultas = []

if not LEADS_CSV.exists():
    print('Sem leads capturados no momento.')
    raise SystemExit(0)

with LEADS_CSV.open('r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, start=1):
        consultas.append({
            'nome': row.get('nome') or row.get('NOME') or '',
            'email': row.get('email') or row.get('EMAIL') or '',
            'whatsapp': row.get('whatsapp') or row.get('WHATSAPP') or '',
            'cidade': row.get('cidade') or row.get('CIDADE') or '',
            'interesse': row.get('interesse') or row.get('INTERESSE') or row.get('assunto') or '',
            'origem': row.get('origem') or row.get('ORIGEM') or 'site',
            'empresa': row.get('empresa') or row.get('EMPRESA') or '',
        })

if not consultas:
    print('0 leads processados.')
    raise SystemExit(0)

# Gera CSV do dia
with OUT_CSV.open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['nome','email','whatsapp','cidade','interesse','origem','empresa','data'])
    writer.writeheader()
    for row in consultas:
        writer.writerow({**row, 'data': hoje})

# Gera follow-ups HTML/TXT por lead
followups = []
for idx, row in enumerate(consultas[:10], start=1):
    nome = row['nome'] or 'Lead'
    cidade = row['cidade']
    interesse = row['interesse']
    empresa = row['empresa']
    email = row['email']
    assunto = f"Parceria Praia Digital — {cidade or 'Litoral'}"
    saudacao = (
        f"Ola, {nome}! Vi que voce tem interesse em \"{interesse}\" "
        f"e atuamos com parcerias de IA para imobiliarias em {cidade or 'o litoral paulista'}."
    )
    corpo = (
        f"{saudacao}\n\n"
        f"Temos opcoes de captacao, avaliacao de precos e atendimento automatico 24h.\n"
        f"Se quiser, posso enviar uma proposta rapida para {empresa or 'sua imobiliaria'}.\n\n"
        f"Responda este e-mail ou chame no WhatsApp para agendar uma demonstracao de 15 minutos.\n"
    )
    followups.append({
        'nome': nome,
        'assunto': assunto,
        'corpo': corpo,
        'email': email,
    })

# Atualiza tracker de follow-up
if not TRACKER.exists():
    TRACKER.write_text('', encoding='utf-8')
linhas = TRACKER.read_text(encoding='utf-8').splitlines()

novas = []
for idx, row in enumerate(consultas, start=1):
    status = 'pendente_envio'
    prioridade = 'Alta' if row.get('cidade') in ['Santos','Guaruja','Ubatuba','Ilhabela'] else 'Media'
    novas.append(f"| {hoje} | {row['nome']} | {row['email']} | {row['cidade']} | {row['interesse']} | {status} | {prioridade} | contato_manual_d3 |")

if novas:
    TRACKER.write_text('\n'.join(linhas + novas + ['']), encoding='utf-8')

# follow-ups por lead em outreach/followups-pendentes/
for idx, row in enumerate(consultas[:10], start=1):
    nome = row['nome'] or 'Lead'
    cidade = row['cidade']
    interesse = row['interesse']
    empresa = row['empresa']
    email = row['email']
    assunto = f"Parceria Praia Digital — {cidade or 'Litoral'}"
    saudacao = (
        f"Ola, {nome}! Vi que voce tem interesse em \"{interesse}\" "
        f"e atuamos com parcerias de IA para imobiliarias em {cidade or 'o litoral paulista'}."
    )
    corpo = (
        f"{saudacao}\n\n"
        f"Temos opcoes de captacao, avaliacao de precos e atendimento automatico 24h.\n"
        f"Se quiser, posso enviar uma proposta rapida para {empresa or 'sua imobiliaria'}.\n\n"
        f"Responda este e-mail ou chame no WhatsApp para agendar uma demonstracao de 15 minutos.\n"
    )
    arq = OUT_DIR / f"followup-pendente-site-{idx:03d}-{nome.split()[0].lower() if nome.split() else 'lead'}.txt"
    arq.write_text(f"Assunto: {assunto}\nDestino: {email}\n\n{corpo}", encoding='utf-8')

print(f"Leads processados: {len(consultas)}")
print(f"Follow-ups gerados: {len(followups)}")
print(f"Saída: {OUT_CSV}")
