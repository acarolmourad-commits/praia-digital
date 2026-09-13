#!/usr/bin/env python3
"""
Preencher msg1 nos CSVs de whatsapp para Consultoria e Avaliacao de Preco.
Gera templates personalizados por cidade/segmento.
"""
import csv, os, json
from datetime import date

BASE = "C:/Users/Carolina/praia-digital"
B2B_DIR = os.path.join(BASE, "docs/sales/csv-lotes-b2b")
TODAY = "2026-09-13"

def load_csv(path):
    with open(path, 'r', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f, delimiter=';'))

def save_csv(path, rows):
    if not rows:
        return
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter=';')
        w.writeheader()
        w.writerows(rows)

# Templates por tipo
TEMPLATES = {
    'consultoria': {
        'default': 'Olá {nome}, sou da Praia Digital. Temos uma consultoria exclusiva para {cidade} sobre gestão e captação de imóveis para temporada. Posso agendar uma apresentação? 🏠',
        'praia_grande': 'Olá {nome}, praia.digital aqui. Temos oportunidades de investimento em Praia Grande com ROI de até 12% em aluguel temporada. Quer ver o tour virtual 360° do imóvel? 🏖️',
        'guarujá': 'Olá {nome}, Guarujá está em alta para segunda residência em 2026. Podemos apresentar oportunidades com tour virtual 360° e comparativo de m²? 📊',
        'santos': 'Olá {nome}, Santos tem valorização de +5,2% no m² em 2026. Temos consultoria gratuita para imobiliárias da região. Agendamos uma call? 📈',
    },
    'avaliacao': {
        'default': 'Olá {nome}, praia.digital aqui. Fazemos avaliação gratuita do seu imóvel em {cidade}. Quer receber um comparativo de preço? 🏠',
        'praia_grande': 'Olá {nome}, precisando vender em Praia Grande? Fazemos avaliação comparativa com dados reais do mercado 2026. É gratuito e sem compromisso. 📊',
        'guarujá': 'Olá {nome}, imóvel no Guarujá? Avaliamos com base em vendas recentes e tour virtual 360° para acelerar a venda. Posso enviar uma estimativa? 🏖️',
        'santos': 'Olá {nome}, Santos valorizou +5,2% no m² em 2026. Fazemos avaliação gratuita do seu imóvel com dados atualizados do mercado. 📈',
    }
}

def get_template(tipo, cidade):
    """Get the best template for the city"""
    templates = TEMPLATES.get(tipo, {})
    cidade_lower = cidade.lower().strip() if cidade else ''
    
    # Exact match
    for key, template in templates.items():
        if key in cidade_lower:
            return template
    
    # Default
    return templates.get('default', 'Olá {nome}, temos uma oportunidade para {cidade}. Podemos conversar? 📞')

def fill_msg1(rows, tipo):
    """Fill msg1 for rows"""
    updated = 0
    for row in rows:
        nome = row.get('nome', '')
        cidade = row.get('cidade', '')
        template = get_template(tipo, cidade)
        row['msg1'] = template.format(nome=nome, cidade=cidade)
        updated += 1
    return updated

def main():
    print("=== PREENCHER MSG1 WHATSAPP ===\n")
    
    for tipo in ['consultoria', 'avaliacao']:
        pw_path = os.path.join(B2B_DIR, f'para-whatsapp-{tipo}-{TODAY}.csv')
        if not os.path.exists(pw_path):
            print(f"❌ {tipo}: arquivo nao encontrado")
            continue
        
        rows = load_csv(pw_path)
        n = fill_msg1(rows, tipo)
        
        # Backup original
        backup_path = pw_path.replace('.csv', f'-backup-{TODAY}.csv')
        import shutil
        shutil.copy2(pw_path, backup_path)
        
        # Save updated
        save_csv(pw_path, rows)
        
        print(f"✅ WhatsApp {tipo}: {n} msg1 preenchidas")
        for i, row in enumerate(rows[:3]):
            print(f"   {row.get('nome', '')}: {row.get('msg1', '')[:60]}...")
        print()
    
    print("=== VALIDACAO ===")
    for tipo in ['consultoria', 'avaliacao']:
        pw_path = os.path.join(B2B_DIR, f'para-whatsapp-{tipo}-{TODAY}.csv')
        rows = load_csv(pw_path)
        com_msg1 = sum(1 for r in rows if r.get('msg1', '').strip())
        print(f"{tipo}: {com_msg1}/{len(rows)} com msg1 preenchida")

if __name__ == "__main__":
    main()