#!/usr/bin/env python3
"""
Follow-up automático D2/D5/D10 — verificação diária
Regras:
- Resposta negativa → encerrar
- Pedido para parar → bloquear
- Interessado/preço/agendamento → HANDOFF + parar follow-up
- Sem resposta → enviar próxima mensagem da sequência
"""
import csv
from pathlib import Path
from datetime import datetime, date

BASE = Path(__file__).resolve().parent.parent / 'docs' / 'comercial'
LEADS_PATH = BASE / 'leads_sao_sebastiao_bertioga.csv'
METRICS_PATH = BASE / 'metricas_comerciais_2026-08-15.md'

TODAY = date.today()

def parse_date(s):
    if not s:
        return None
    try:
        return datetime.strptime(s, '%Y-%m-%d').date()
    except ValueError:
        return None

def days_since(d):
    if not d:
        return None
    return (TODAY - d).days

def main():
    with LEADS_PATH.open(encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # Ensure new columns exist
    for col in ['resposta','data_resposta','tipo_resposta','servico_interesse','valor_potencial','estagio','proxima_acao','responsavel','objeção']:
        if col not in fieldnames:
            fieldnames.append(col)

    today_str = TODAY.isoformat()
    metrics = {
        'respostas': 0,
        'positivas': 0,
        'precos': 0,
        'agendamentos': 0,
        'encerrados': 0,
        'bloqueados': 0,
        'handoffs': 0,
    }

    for row in rows:
        status = row.get('status', '')
        lead_id = row.get('lead_id', '')
        d0 = parse_date(row.get('d0_enviado_em'))
        d2 = parse_date(row.get('d2_enviado_em'))
        d5 = parse_date(row.get('d5_enviado_em'))
        d10 = parse_date(row.get('d10_enviado_em'))

        # Skip if already completed/handoff/blocked
        if status in ['ENCERRADO','BLOQUEADO','HANDOFF','VENDIDO']:
            continue

        # Check for response
        resposta = row.get('resposta', '').strip()
        tipo = row.get('tipo_resposta', '').strip()

        if resposta:
            metrics['respostas'] += 1
            if tipo == 'positiva':
                metrics['positivas'] += 1
                row['status'] = 'HANDOFF'
                row['estagio'] = 'HANDOFF_HUMANO'
                row['proxima_acao'] = 'Humano deve entrar em contato'
                row['responsavel'] = 'Humano'
                metrics['handoffs'] += 1
            elif tipo == 'preco':
                metrics['precos'] += 1
                # Continue follow-up, will be handled by human
            elif tipo == 'agendamento':
                metrics['agendamentos'] += 1
                row['status'] = 'HANDOFF'
                row['estagio'] = 'AGENDAMENTO_HUMANO'
                row['proxima_acao'] = 'Humano deve confirmar agenda'
                row['responsavel'] = 'Humano'
                metrics['handoffs'] += 1
            elif tipo == 'negativa':
                row['status'] = 'ENCERRADO'
                metrics['encerrados'] += 1
            elif tipo == 'bloqueio':
                row['status'] = 'BLOQUEADO'
                metrics['bloqueados'] += 1
            continue

        # No response yet — check if we need to send next follow-up
        if status == 'ENVIADO_D0' and d0 and days_since(d0) >= 2 and not d2:
            # Prepare D2
            row['d2_enviado_em'] = today_str
            row['status'] = 'ENVIADO_D2'
            print(f'D2 ready for lead {lead_id}')
        elif status == 'ENVIADO_D2' and d2 and days_since(d2) >= 3 and not d5:
            row['d5_enviado_em'] = today_str
            row['status'] = 'ENVIADO_D5'
            print(f'D5 ready for lead {lead_id}')
        elif status == 'ENVIADO_D5' and d5 and days_since(d5) >= 5 and not d10:
            row['d10_enviado_em'] = today_str
            row['status'] = 'ENVIADO_D10'
            print(f'D10 ready for lead {lead_id}')

    # Write back
    with LEADS_PATH.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print('Metrics:', metrics)

if __name__ == '__main__':
    main()
