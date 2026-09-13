#!/usr/bin/env python3
"""
Disparo de campanhas via Brevo (email marketing).
Valida CSVs, envia via API Brevo e registra log.
"""
import csv, os, json, urllib.request
from datetime import date

BASE = "C:/Users/Carolina/praia-digital"
B2B_DIR = os.path.join(BASE, "docs/sales/csv-lotes-b2b")
LOG_DIR = os.path.join(BASE, "docs/sales/logs")
TODAY = "2026-09-13"

BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "")
BREVO_API_URL = "https://api.brevo.com/v3/contacts/import"

def load_csv(path):
    with open(path, 'r', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f, delimiter=';'))

def send_brevo_csv(tipo, rows):
    """Send CSV to Brevo API"""
    if not BREVO_API_KEY:
        return {"status": "skipped", "reason": "BREVO_API_KEY not set"}
    
    # Prepare contacts
    contacts = []
    for row in rows:
        contacts.append({
            "email": row.get('email', ''),
            "attributes": {
                "NOME": row.get('nome', ''),
                "TELEFONE": row.get('telefone', ''),
                "CIDADE": row.get('cidade', ''),
                "IMOBILIARIA": row.get('imobiliaria', ''),
                "TIPO": tipo,
            }
        })
    
    payload = json.dumps({"contacts": contacts, "updateExisting": True})
    
    req = urllib.request.Request(
        BREVO_API_URL,
        data=payload.encode('utf-8'),
        headers={
            "api-key": BREVO_API_KEY,
            "Content-Type": "application/json"
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return {"status": "sent", "code": resp.status, "body": resp.read().decode()}
    except Exception as e:
        return {"status": "error", "reason": str(e)}

def main():
    os.makedirs(LOG_DIR, exist_ok=True)
    
    print("=== DISPARO BREVO - CONSULTORIA E AVALIACAO ===\n")
    
    for tipo in ['consultoria', 'avaliacao']:
        pb_path = os.path.join(B2B_DIR, f'para-brevo-{tipo}-{TODAY}.csv')
        if not os.path.exists(pb_path):
            print(f"❌ {tipo}: CSV nao encontrado")
            continue
        
        rows = load_csv(pb_path)
        print(f"📧 Brevo {tipo}: {len(rows)} leads")
        
        # Send
        result = send_brevo_csv(tipo, rows)
        print(f"   Result: {result['status']}")
        
        if result['status'] == 'sent':
            print(f"   ✅ Disparado com sucesso")
        elif result['status'] == 'skipped':
            print(f"   ⚠️  Pulado: {result.get('reason', '')}")
        else:
            print(f"   ❌ Erro: {result.get('reason', '')}")
        
        # Log
        log_path = os.path.join(LOG_DIR, f"brevo-{tipo}-{TODAY}-disparo.json")
        with open(log_path, 'w') as f:
            json.dump({
                'tipo': tipo,
                'data': TODAY,
                'total': len(rows),
                'result': result
            }, f, indent=2)
        print()
    
    print("=== RESUMO ===")
    print("Disparos Brevo processados para Consultoria e Avaliacao de Preco")
    print("Verifique logs em docs/sales/logs/ para confirmacoes detalhadas")

if __name__ == "__main__":
    main()