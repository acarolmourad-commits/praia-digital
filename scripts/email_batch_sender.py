
import csv
import smtplib
import os
import time
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configurações SMTP (preencher com credenciais reais antes de execução)
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
FROM_NAME = 'Carolina Moura'
FROM_EMAIL = os.getenv('SMTP_FROM', SMTP_USER)
BATCH_SIZE = 10  # Enviar em lotes para evitar bloqueio
DELAY_BETWEEN = 5  # segundos entre e-mails

LEADS_CSV = 'docs/sales/leads-litoral-enriquecido.csv'
OUTREACH_DIR = 'outreach'
SENT_LOG = 'docs/sales/email-sent-log.csv'

def load_leads():
    leads = []
    with open(LEADS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row.get('email', '').strip()
            if email and '@' in email:
                leads.append({
                    'id': row.get('id', ''),
                    'nome': row.get('nome', f"Lead {row.get('id', '')}"),
                    'email': email,
                    'cidade': row.get('cidade', 'Litoral'),
                    'bairro': row.get('bairro', row.get('cidade', 'Litoral'))
                })
    return leads

def load_outreach_leads_sent():
    sent = set()
    if os.path.exists('docs/sales/outreach-enviados.csv'):
        with open('docs/sales/outreach-enviados.csv', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                if parts:
                    sent.add(parts[0])
    return sent

def create_email_content(lead):
    subject = f"Parceria com IA para {lead['bairro']}/{lead['cidade']} — Praia Digital"
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<body style="font-family:'Segoe UI',system-ui,sans-serif;background:#F4EBD0;color:#023047;margin:0;padding:20px">
<div style="max-width:650px;margin:0 auto;background:#fff;border-radius:16px;padding:2rem;box-shadow:0 4px 12px rgba(0,0,0,.08)">
  <h2 style="color:#0077B6">Olá, {lead['nome']}!</h2>
  <p>Sou <strong>Carolina Moura</strong>, CEO da <strong>Praia Digital</strong>.</p>
  <p>Imóveis no litoral paulista exigem <strong>rapidez</strong>, <strong>avaliação precisa</strong> e <strong>atendimento inteligente</strong> para transformar visitas em vendas.</p>
  <p>A Praia Digital entrega ferramentas de IA para:</p>
  <ul>
    <li>Avaliação automática de preço</li>
    <li>Geração de descrições otimizadas</li>
    <li>Qualificação de leads por temperatura</li>
    <li>Roteiro de compradores personalizado</li>
  </ul>
  <p><strong>Sem custo inicial</strong>. Você foca no relacionamento; nós entregamos a inteligência.</p>
  <p style="text-align:center"><a href="https://praia.digital" style="background:#0077B6;color:#fff;padding:12px 24px;border-radius:50px;text-decoration:none;font-weight:700">Experimente grátis</a></p>
  <p style="font-size:0.85rem;color:#666">CEO Carolina Moura | (11) 95434-6288 | comercial@praia.digital</p>
</div>
</body>
</html>"""
    return subject, html

def send_batch(leads_batch):
    if not SMTP_USER or not SMTP_PASSWORD:
        print("[SIMULAÇÃO] SMTP não configurado. Rodando em modo simulação.")
        return []
    
    sent_ids = []
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            
            for lead in leads_batch:
                try:
                    subject, html = create_email_content(lead)
                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = subject
                    msg['From'] = f"{FROM_NAME} <{FROM_EMAIL}>"
                    msg['To'] = lead['email']
                    msg['Reply-To'] = 'comercial@praia.digital'
                    part = MIMEText(html, 'html', 'utf-8')
                    msg.attach(part)
                    server.sendmail(FROM_EMAIL, lead['email'], msg.as_string())
                    sent_ids.append(lead['id'])
                    log_sent(lead, subject)
                    print(f"  ✓ Enviado para {lead['email']}")
                    time.sleep(DELAY_BETWEEN)
                except Exception as e:
                    print(f"  ✗ Erro ao enviar para {lead['email']}: {e}")
    except Exception as e:
        print(f"Erro SMTP: {e}")
    return sent_ids

def log_sent(lead, subject):
    with open('docs/sales/outreach-enviados.csv', 'a', encoding='utf-8') as f:
        f.write(f"{lead['id']},{lead['email']},{datetime.now().isoformat()},{subject}\n")

if __name__ == '__main__':
    all_leads = load_leads()
    sent_ids = load_outreach_leads_sent()
    pending = [l for l in all_leads if l['id'] not in sent_ids]
    print(f"Total leads: {len(all_leads)}")
    print(f"Já enviados: {len(sent_ids)}")
    print(f"Pendentes: {len(pending)}")
    
    if not pending:
        print("Nenhum lead pendente para envio.")
        exit(0)
    
    total_sent = 0
    for i in range(0, len(pending), BATCH_SIZE):
        batch = pending[i:i+BATCH_SIZE]
        print(f"\nEnviando lote {i//BATCH_SIZE + 1} ({len(batch)} e-mails)...")
        sent = send_batch(batch)
        total_sent += len(sent)
        if i + BATCH_SIZE < len(pending):
            print(f"Aguardando 30s antes do próximo lote...")
            time.sleep(30)
    
    print(f"\nConcluído. Total enviado: {total_sent}/{len(pending)}")
