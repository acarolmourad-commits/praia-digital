#!/usr/bin/env python3
"""
litoral_followup.py
Envia follow-up automático via WhatsApp para leads da Litoral Prime.
Uso: python litoral-prime-imoveis/automation/litoral_followup.py
"""
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parents[1]
LEADS_FILE = BASE / 'docs/leads-litoral-prime.csv'
TRACKER_FILE = BASE / 'docs/tracker-litoral-prime.csv'

MENSAGENS = {
    'comprar': 'Olá! Vi que você tem interesse em comprar um imóvel no litoral de SP. Posso enviar as melhores opções?',
    'alugar': 'Olá! Vi que você tem interesse em alugar um imóvel no litoral de SP. Podemos ajudar?',
    'vender': 'Olá! Vi que você quer vender um imóvel no litoral de SP. Quer uma avaliação gratuita?',
}

def enviar_whatsapp(telefone, mensagem):
    """Simula envio de WhatsApp. Integração real via Twilio/WhatsApp Business API."""
    print(f"[WhatsApp] Enviando para {telefone}: {mensagem}")
    # Integração: aqui você colocaria a chamada real para WhatsApp Business API

def processar_novos_leads():
    """Processa leads pendentes e envia follow-up."""
    if not LEADS_FILE.exists():
        print("[Litoral Prime] Nenhum lead para processar.")
        return
    
    leads = []
    with LEADS_FILE.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            leads.append(row)
    
    processados = 0
    for lead in leads:
        interesse = lead.get('interesse', '')
        telefone = lead.get('telefone', '')
        nome = lead.get('nome', '')
        
        if not telefone or not interesse:
            continue
        
        mensagem = MENSAGENS.get(interesse, 'Olá! Entraremos em contato em breve.')
        enviar_whatsapp(telefone, mensagem)
        processados += 1
    
    print(f"[Litoral Prime] Follow-up enviado para {processados} leads.")

if __name__ == '__main__':
    processar_novos_leads()
