#!/usr/bin/env python3
"""
Execução automática do D2 do Motor A — 2026-08-17 09:00.
Uso: python scripts/executar_d2_2026-08-17.py
"""

import csv
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = Path('C:/Users/Carolina/praia-digital')
LEADS_PATH = REPO / 'docs/comercial/leads_sao_sebastiao_bertioga.csv'
RESULTADO_PATH = REPO / 'docs/comercial/resultado_d2_2026-08-17.md'
ORDEM = ['9', '11', '14', '15', '27', '29']
DATA_HOJE = '2026-08-17'


def run(cmd, cwd=REPO):
    print(f'>>> {cmd}')
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.returncode != 0:
        print('STDERR:', result.stderr)
    return result.returncode


def main():
    print('=== D2 Motor A — Execução automática ===')
    print(f'Data/hora: {datetime.now().isoformat()}')

    # 1. Ler leads
    with LEADS_PATH.open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    d2_leads = {r['lead_id']: r for r in rows if r.get('status') == 'ENVIADO_D0' and r.get('d0_enviado_em') == '2026-08-15'}
    print(f'Leads ENVIADO_D0 elegíveis: {len(d2_leads)}')

    missing = [lid for lid in ORDEM if lid not in d2_leads]
    if missing:
        print(f'ERRO: leads faltando para D2: {missing}')
        sys.exit(1)

    # 2. Verificar pré-condições
    print('\n--- Verificação pré-D2 ---')
    respostas = sum(1 for r in rows if r.get('resposta'))
    print(f'Respostas registradas: {respostas}')
    if respostas > 0:
        print('AVISO: existem respostas; verificar antes de prosseguir.')
        # Não interrompe; apenas alerta

    # 3. Atualizar CRM
    print('\n--- Atualizando CRM ---')
    updated = 0
    for lid in ORDEM:
        r = d2_leads[lid]
        r['status'] = 'ENVIADO_D2'
        r['d2_enviado_em'] = DATA_HOJE
        updated += 1

    fieldnames = rows[0].keys()
    with LEADS_PATH.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f'Leads atualizados para ENVIADO_D2: {updated}')

    # 4. Gerar resultado
    print('\n--- Gerando resultado D2 ---')
    resultado = RESULTADO_PATH.read_text(encoding='utf-8')
    for lid in ORDEM:
        r = d2_leads[lid]
        # Preencher tabela de status do disparo
        marker = f'| {lid} |'
        replacement = f'| {lid} | {r.get("canal_contato","")} | {DATA_HOJE} | | | | | | | | |'
        resultado = resultado.replace(marker, replacement)

    RESULTADO_PATH.write_text(resultado, encoding='utf-8')
    print('Resultado D2 atualizado.')

    # 5. Rodar automações
    print('\n--- Rodando automações ---')
    run('python scripts/follow_up_automacao.py')
    run('python scripts/relatorio_diario_motor_b.py')

    # 6. Commit
    print('\n--- Commit ---')
    run('git add docs/comercial/leads_sao_sebastiao_bertioga.csv docs/comercial/resultado_d2_2026-08-17.md')
    run('git commit -m "feat: publicar Batch D2 — 6 leads enviados e atualizar resultado/CRM 2026-08-17"')

    print('\n=== D2 concluído ===')


if __name__ == '__main__':
    main()
