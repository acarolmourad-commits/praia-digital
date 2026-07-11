"""Verifica saúde da prospecção:
- Follow-ups atrasados
- Leads sem envio registrado
- Inconsistências no tracker
Saída: relatório simple em stdout
"""
from pathlib import Path
from datetime import datetime

ROOT = Path('C:/Users/Carolina/praia-digital')
tracker = ROOT / 'docs/sales/tracking-envios-lote-50-2026-07-12.csv'
hoje = datetime.now().strftime('%Y-%m-%d')

def main():
    if not tracker.exists():
        print('Tracker não encontrado:', tracker)
        return
    import csv
    rows = []
    with tracker.open('r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f, delimiter=';'))
    atrasados = []
    sem_envio = []
    for r in rows:
        data_envio = r.get('data_envio','').strip()
        data_proxima = r.get('data_proxima_acao','').strip()
        status_envio = r.get('status_envio','').strip().lower()
        if status_envio not in ('enviado','enviada'):
            sem_envio.append(r)
        if data_proxima and data_proxima < hoje:
            atrasados.append(r)
    print('Total leads:', len(rows))
    print('Sem envio:', len(sem_envio))
    print('Follow-ups atrasados:', len(atrasados))
    if sem_envio:
        ids = [r.get('lead_id') for r in sem_envio[:10]]
        print('Sem envio (até 10):', ids)
    if atrasados:
        ids = [r.get('lead_id') for r in atrasados[:10]]
        print('Atrasados (até 10):', ids)

if __name__ == '__main__':
    main()
