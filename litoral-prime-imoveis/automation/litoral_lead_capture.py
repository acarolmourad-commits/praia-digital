#!/usr/bin/env python3
"""
litoral_lead_capture.py
Capta leads do site Litoral Prime e registra para follow-up automático.
Uso: python litoral-prime-imoveis/automation/litoral_lead_capture.py
"""
import csv
import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parents[1]
LEADS_FILE = BASE / 'docs/leads-litoral-prime.csv'
TRACKER_FILE = BASE / 'docs/tracker-litoral-prime.csv'

LEADS_FILE.parent.mkdir(parents=True, exist_ok=True)

def capturar_lead(nome, email, telefone, interesse, mensagem=''):
    """Captura um novo lead e registra no tracker."""
    hoje = datetime.now().strftime('%Y-%m-%d')
    lead_id = datetime.now().strftime('%Y%m%d%H%M%S')
    
    # Salvar lead
    with LEADS_FILE.open('a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        if LEADS_FILE.stat().st_size == 0:
            writer.writerow(['lead_id', 'nome', 'email', 'telefone', 'interesse', 'mensagem', 'data_criacao'])
        writer.writerow([lead_id, nome, email, telefone, interesse, mensagem, hoje])
    
    # Atualizar tracker
    with TRACKER_FILE.open('a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        if TRACKER_FILE.stat().st_size == 0:
            writer.writerow(['lead_id', 'nome', 'interesse', 'status', 'data_envio', 'observacao'])
        writer.writerow([lead_id, nome, interesse, 'novo', hoje, ''])
    
    print(f"[Litoral Prime] Lead capturado: {nome} - {interesse}")
    return lead_id

if __name__ == '__main__':
    # Teste
    capturar_lead('Teste', 'teste@email.com', '(11) 99999-9999', 'comprar', 'Tenho interesse em apto 2qtos')
