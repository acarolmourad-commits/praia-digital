#!/usr/bin/env python3
"""
sistema_referral.py
Sistema de indicação com recompensa para Litoral Prime.
Uso: python litoral-prime-imoveis/automation/sistema_referral.py
"""
import csv
import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parents[1]
REFERRALS_FILE = BASE / 'docs/referrals.csv'
REWARDS_FILE = BASE / 'docs/rewards.json'

REFERRALS_FILE.parent.mkdir(parents=True, exist_ok=True)

REWARDS = {
    'compra': {'valor': 2000, 'descricao': 'R$ 2.000 em dinheiro'},
    'aluguel': {'valor': 500, 'descricao': 'R$ 500 em dinheiro'},
    'indicacao': {'valor': 300, 'descricao': 'R$ 300 em dinheiro'},
}

def registrar_indicacao(indicador_nome, indicador_telefone, indicado_nome, indicado_telefone, tipo_operacao):
    """Registra uma nova indicação."""
    hoje = datetime.now().strftime('%Y-%m-%d')
    referral_id = datetime.now().strftime('%Y%m%d%H%M%S')
    
    with REFERRALS_FILE.open('a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        if REFERRALS_FILE.stat().st_size == 0:
            writer.writerow(['referral_id', 'indicador_nome', 'indicador_telefone', 'indicado_nome', 'indicado_telefone', 'tipo_operacao', 'data_criacao', 'status', 'recompensa'])
        writer.writerow([referral_id, indicador_nome, indicador_telefone, indicado_nome, indicado_telefone, tipo_operacao, hoje, 'pendente', ''])
    
    recompensa = REWARDS.get(tipo_operacao, REWARDS['indicacao'])
    print(f"[Referral] Indicação registrada: {indicador_nome} -> {indicado_nome} ({tipo_operacao})")
    print(f"[Referral] Recompensa: {recompensa['descricao']}")
    return referral_id, recompensa

def processar_recompensas():
    """Processa indicações fechadas e gera recompensas."""
    if not REFERRALS_FILE.exists():
        return
    
    rewards = []
    with REFERRALS_FILE.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if row.get('status') == 'fechado' and not row.get('recompensa'):
                tipo = row.get('tipo_operacao', 'indicacao')
                recompensa = REWARDS.get(tipo, REWARDS['indicacao'])
                rewards.append({
                    'indicador': row.get('indicador_nome'),
                    'valor': recompensa['valor'],
                    'descricao': recompensa['descricao'],
                    'indicado': row.get('indicado_nome'),
                })
    
    if rewards:
        with REWARDS_FILE.open('w', encoding='utf-8') as f:
            json.dump(rewards, f, ensure_ascii=False, indent=2)
        print(f"[Referral] {len(rewards)} recompensas processadas")
    else:
        print("[Referral] Nenhuma recompensa pendente")

def main():
    print("[Referral] Sistema de indicação Litoral Prime")
    # Exemplo de uso
    registrar_indicacao('João Silva', '(13) 99111-0001', 'Maria Santos', '(13) 99111-0002', 'compra')
    processar_recompensas()

if __name__ == '__main__':
    main()
