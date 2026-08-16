#!/usr/bin/env python3
"""
Registro de eventos do Motor B — Diagnóstico do Anúncio de Temporada 2026.
Eventos: visit, start, item_1..item_15, finish, cta_click, lead_created, d0_sent, d2_sent, d5_sent, d10_sent, response, handoff, sale.
"""
import csv
import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parent.parent / 'docs' / 'comercial'
EVENTS_PATH = BASE / 'diagnostico_eventos_2026.csv'
FUNNEL_PATH = BASE / 'diagnostico_funil_2026.csv'
LEADS_PATH = BASE / 'diagnostico_leads_2026.csv'

EVENT_FIELDS = ['event_id','session_id','timestamp','source','campaign','event','profile_type','score','classification','path','device','notes']
FUNNEL_FIELDS = ['date','source','visits','starts','finishes','cta_clicks','leads','qualified','editions_requested','sales','start_rate','finish_rate','cta_rate','lead_rate','conversion_rate']
LEAD_FIELDS = ['lead_id','created_at','source','campaign','score','classification','path','name','contact','city','neighborhood','property_type','status','d0_sent','d2_sent','d5_sent','d10_sent','response','response_type','edition_requested','sale','notes']

def now_iso():
    return datetime.now().isoformat()

def log_event(session_id, event, source='organic', campaign='diagnostico-direct', profile_type='', score='', classification='', path='', device='web', notes=''):
    with EVENTS_PATH.open('a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=EVENT_FIELDS)
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow({
            'event_id': f"{session_id[:8]}-{event}",
            'session_id': session_id,
            'timestamp': now_iso(),
            'source': source,
            'campaign': campaign,
            'event': event,
            'profile_type': profile_type,
            'score': score,
            'classification': classification,
            'path': path,
            'device': device,
            'notes': notes,
        })

def create_lead(session_id, source, campaign, score, classification, path, name='', contact='', city='', neighborhood='', property_type='', notes=''):
    lead_id = f"LEAD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    with LEADS_PATH.open('a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=LEAD_FIELDS)
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow({
            'lead_id': lead_id,
            'created_at': now_iso(),
            'source': source,
            'campaign': campaign,
            'score': score,
            'classification': classification,
            'path': path,
            'name': name,
            'contact': contact,
            'city': city,
            'neighborhood': neighborhood,
            'property_type': property_type,
            'status': 'CRIADO',
            'd0_sent': '',
            'd2_sent': '',
            'd5_sent': '',
            'd10_sent': '',
            'response': '',
            'response_type': '',
            'edition_requested': '',
            'sale': '',
            'notes': notes,
        })
    log_event(session_id, 'lead_created', source, campaign, score=score, classification=classification, path=path, notes=f"lead_id={lead_id}")
    return lead_id

def update_daily_funnel(date_str, source, visits, starts, finishes, cta_clicks, leads, qualified=0, editions=0, sales=0):
    start_rate = f"{starts/visits*100:.1f}%" if visits else '0%'
    finish_rate = f"{finishes/starts*100:.1f}%" if starts else '0%'
    cta_rate = f"{cta_clicks/finishes*100:.1f}%" if finishes else '0%'
    lead_rate = f"{leads/cta_clicks*100:.1f}%" if cta_clicks else '0%'
    conv_rate = f"{sales/leads*100:.1f}%" if leads else '0%'
    with FUNNEL_PATH.open('a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FUNNEL_FIELDS)
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow({
            'date': date_str,
            'source': source,
            'visits': visits,
            'starts': starts,
            'finishes': finishes,
            'cta_clicks': cta_clicks,
            'leads': leads,
            'qualified': qualified,
            'editions_requested': editions,
            'sales': sales,
            'start_rate': start_rate,
            'finish_rate': finish_rate,
            'cta_rate': cta_rate,
            'lead_rate': lead_rate,
            'conversion_rate': conv_rate,
        })

if __name__ == '__main__':
    # Exemplo: simular sessão
    sid = 'session-' + datetime.now().strftime('%Y%m%d%H%M%S')
    log_event(sid, 'visit', source='organic', campaign='diagnostico-direct')
    log_event(sid, 'start', source='organic', campaign='diagnostico-direct')
    log_event(sid, 'finish', source='organic', campaign='diagnostico-direct', score='58', classification='🟡 Anúncio com oportunidades', path='Caminho 2')
    log_event(sid, 'cta_click', source='organic', campaign='diagnostico-direct', score='58', classification='🟡 Anúncio com oportunidades', path='Caminho 2')
    create_lead(sid, 'organic', 'diagnostico-direct', '58', '🟡 Anúncio com oportunidades', 'Caminho 2', name='Teste', contact='test@example.com', city='São Sebastião', neighborhood='Praia da Baleia', property_type='Casa', notes='Lead simulado Fase 5')
    update_daily_funnel(datetime.now().isoformat()[:10], 'organic', 1, 1, 1, 1, 1, 0, 0, 0)
    print('Eventos registrados com sucesso.')
