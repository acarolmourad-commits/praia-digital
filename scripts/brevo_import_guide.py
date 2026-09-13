#!/usr/bin/env python3
"""
Gera passo a passo para importar CSV no Brevo (web interface).
Uso: python scripts/brevo_import_guide.py
"""
import os, csv
from datetime import date

BASE = "C:/Users/Carolina/praia-digital"
B2B_DIR = os.path.join(BASE, "docs/sales/csv-lotes-b2b")
GUIAS_DIR = os.path.join(BASE, "docs/sales/guias")
TODAY = "2026-09-13"

def gerar_guias():
    os.makedirs(GUIAS_DIR, exist_ok=True)
    
    for tipo in ['consultoria', 'avaliacao']:
        csv_file = f"para-brevo-{tipo}-{TODAY}.csv"
        csv_path = os.path.join(B2B_DIR, csv_file)
        
        if not os.path.exists(csv_path):
            print(f"❌ {csv_file} nao encontrado")
            continue
        
        # Read data
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            rows = list(reader)
        
        guide = f"""# Importar CSV Brevo - {tipo.capitalize()} - {TODAY}

## Passo a passo

1. Acesse: https://app.brevo.com/contacts/import
2. Clique em "Importar contatos"
3. Selecione o arquivo: {csv_file}
4. Delimitador: ponto e vírgula (;)
5. Mapeie colunas:
   - nome → Nome
   - email → Email
   - telefone → Telefone
   - cidade → Cidade
   - imobiliaria → Empresa
6. Marque "Atualizar contatos existentes"
7. Clique em "Importar"

## Arquivo
Caminho: {csv_path}
Total de leads: {len(rows)}

## Dados
"""
        for i, row in enumerate(rows, 1):
            guide += f"{i}. {row.get('nome', '')} - {row.get('email', '')} - {row.get('telefone', '')}\n"
        
        guide_path = os.path.join(GUIAS_DIR, f"brevo-import-{tipo}-{TODAY}.md")
        with open(guide_path, 'w') as f:
            f.write(guide)
        
        print(f"✅ Guia gerado: {guide_path}")

if __name__ == "__main__":
    gerar_guias()