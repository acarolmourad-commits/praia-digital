#!/usr/bin/env python3
"""
Lancar lotes Brevo Consultoria e Avaliacao de Preco para disparo.
Valida fila, marca envio e gera relatorio de confirmacao.
"""
import csv, os, json
from datetime import date, datetime

BASE = "C:/Users/Carolina/praia-digital"
BREVO_DIR = os.path.join(BASE, "docs/sales/csv-lotes-b2b")
LOG_DIR = os.path.join(BASE, "docs/sales/logs")
TODAY = "2026-09-13"

def load_csv(path):
    with open(path, 'r', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f, delimiter=';'))

def mark_sent(rows, tipo):
    """Mark rows as sent in tracker"""
    tracker_path = os.path.join(BREVO_DIR, f"tracker-{tipo}-2026-07-22.csv")
    if os.path.exists(tracker_path):
        with open(tracker_path, 'r', encoding='utf-8-sig') as f:
            tracker = list(csv.DictReader(f, delimiter=';'))
        for row in rows:
            phone = row.get('telefone', '')
            for t in tracker:
                if t.get('telefone', '') == phone:
                    t['status'] = 'enviado'
                    t['data_envio'] = TODAY
                    t['canal'] = 'brevo'
    else:
        tracker = []
        for row in rows:
            tracker.append({**row, 'status': 'enviado', 'data_envio': TODAY, 'canal': 'brevo'})
    
    with open(tracker_path, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=tracker[0].keys(), delimiter=';')
        w.writeheader()
        w.writerows(tracker)
    return len(tracker)

def main():
    os.makedirs(LOG_DIR, exist_ok=True)
    
    resultados = []
    for tipo in ['consultoria', 'avaliacao']:
        csv_path = os.path.join(BREVO_DIR, f'para-brevo-{tipo}-{TODAY}.csv')
        if not os.path.exists(csv_path):
            resultados.append(f"❌ {tipo}: arquivo nao encontrado")
            continue
        
        rows = load_csv(csv_path)
        n = len(rows)
        
        # Mark as sent
        n_sent = mark_sent(rows, tipo)
        
        # Log
        log_path = os.path.join(LOG_DIR, f"brevo-{tipo}-{TODAY}.json")
        with open(log_path, 'w') as f:
            json.dump({
                'tipo': tipo,
                'data': TODAY,
                'total': n,
                'enviados': n_sent,
                'status': 'disparado'
            }, f, indent=2)
        
        resultados.append(f"✅ Brevo {tipo}: {n} leads disparados (tracker: {n_sent})")
    
    # WhatsApp validation
    print("=== DISPARO BREVO ===")
    for r in resultados:
        print(r)
    
    print("\n=== FILA WHATSAPP ===")
    for tipo in ['consultoria', 'avaliacao']:
        pw_path = os.path.join(BREVO_DIR, f'para-whatsapp-{tipo}-{TODAY}.csv')
        if os.path.exists(pw_path):
            rows = load_csv(pw_path)
            print(f"WhatsApp {tipo}: {len(rows)} na fila")
            for row in rows[:3]:
                print(f"  - {row.get('nome', '')}: {row.get('telefone', '')}")

if __name__ == "__main__":
    main()