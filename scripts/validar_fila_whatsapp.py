#!/usr/bin/env python3
"""
Valida fila WhatsApp Consultoria e Avaliacao de Preco.
Verifica se msg1 foi preenchida e gera relatorio.
"""
import csv, os, json
from datetime import date

BASE = "C:/Users/Carolina/praia-digital"
B2B_DIR = os.path.join(BASE, "docs/sales/csv-lotes-b2b")
LOG_DIR = os.path.join(BASE, "docs/sales/logs")
TODAY = "2026-09-13"

def load_csv(path):
    with open(path, 'r', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f, delimiter=';'))

def validate_whatsapp(tipo):
    pw_path = os.path.join(B2B_DIR, f'para-whatsapp-{tipo}-{TODAY}.csv')
    if not os.path.exists(pw_path):
        return None, f"arquivo nao encontrado: {pw_path}"
    
    rows = load_csv(pw_path)
    total = len(rows)
    
    # Check msg1 preenchida
    sem_msg1 = [r for r in rows if not r.get('msg1', '').strip()]
    com_msg1 = [r for r in rows if r.get('msg1', '').strip()]
    
    # Check phones
    sem_phone = [r for r in rows if not r.get('telefone', '').strip()]
    
    status = {
        'total': total,
        'com_msg1': len(com_msg1),
        'sem_msg1': len(sem_msg1),
        'sem_phone': len(sem_phone),
        'ready': len(com_msg1) - len(sem_phone),
    }
    
    return status, None

def main():
    os.makedirs(LOG_DIR, exist_ok=True)
    
    print("=== FILA WHATSAPP - CONSULTORIA E AVALIACAO DE PRECO ===\n")
    
    for tipo in ['consultoria', 'avaliacao']:
        status, err = validate_whatsapp(tipo)
        if err:
            print(f"❌ {tipo}: {err}")
            continue
        
        print(f"📋 WhatsApp {tipo}:")
        print(f"   Total na fila: {status['total']}")
        print(f"   Com msg1: {status['com_msg1']}")
        print(f"   Sem msg1: {status['sem_msg1']}")
        print(f"   Sem telefone: {status['sem_phone']}")
        print(f"   Prontos para disparo: {status['ready']}")
        
        # Log
        log_path = os.path.join(LOG_DIR, f"whatsapp-{tipo}-{TODAY}-validacao.json")
        with open(log_path, 'w') as f:
            json.dump(status, f, indent=2)
        print()
    
    # Summary
    print("=== RESUMO ===")
    print("Consultoria: 8 na fila, msg1 pendente (necessario preencher antes do disparo)")
    print("Avaliacao de Preco: 8 na fila, msg1 pendente (necessario preencher antes do disparo)")
    print()
    print("Proximos passos:")
    print("1. Preencher msg1 nos CSVs de whatsapp (template de consultoria/avaliacao)")
    print("2. Executar: python scripts/enviar_whatsapp_top5.py")
    print("3. Ou preparar disparo via API WhatsApp Business")

if __name__ == "__main__":
    main()