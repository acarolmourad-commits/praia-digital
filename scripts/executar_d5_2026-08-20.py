#!/usr/bin/env python3
"""
Execução automática do D5 do Motor A — 2026-08-20 09:00.
Uso: python scripts/executar_d5_2026-08-20.py
"""

import csv
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = Path('C:/Users/Carolina/praia-digital')
LEADS_PATH = REPO / 'docs/comercial/leads_sao_sebastiao_bertioga.csv'
RESULTADO_PATH = REPO / 'docs/comercial/resultado_d5_2026-08-20.md'
ORDEM = ['9', '11', '14', '15', '27', '29']
DATA_HOJE = '2026-08-20'
ALLOWED_START = datetime(2026, 8, 20, 9, 0, 0)


def run(cmd, cwd=REPO):
    print(f'>>> {cmd}')
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.returncode != 0:
        print('STDERR:', result.stderr)
    return result.returncode


def main():
    now = datetime.now()
    print('=== D5 Motor A — Execução automática ===')
    print(f'Data/hora atual: {now.isoformat()}')

    if now < ALLOWED_START:
        print(f'BLOQUEIO: D5 só pode ser executado em {ALLOWED_START.isoformat()}.')
        print('Nenhuma alteração foi feita.')
        sys.exit(1)

    with LEADS_PATH.open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    d2_leads = {r['lead_id']: r for r in rows if r.get('status') == 'ENVIADO_D2' and r.get('d2_enviado_em') == '2026-08-17'}
    print(f'Leads ENVIADO_D2 elegíveis: {len(d2_leads)}')

    missing = [lid for lid in ORDEM if lid not in d2_leads]
    if missing:
        print(f'ERRO: leads faltando para D5: {missing}')
        sys.exit(1)

    print('\n--- Verificação pré-D5 ---')
    respostas = sum(1 for r in rows if r.get('resposta'))
    print(f'Respostas registradas: {respostas}')
    if respostas > 0:
        print('AVISO: existem respostas; verificar antes de prosseguir.')

    print('\n--- Atualizando CRM ---')
    updated = 0
    for lid in ORDEM:
        r = d2_leads[lid]
        r['status'] = 'ENVIADO_D5'
        r['d5_enviado_em'] = DATA_HOJE
        updated += 1

    fieldnames = rows[0].keys()
    with LEADS_PATH.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f'Leads atualizados para ENVIADO_D5: {updated}')

    print('\n--- Gerando resultado D5 ---')
    resultado = RESULTADO_PATH.read_text(encoding='utf-8')
    for lid in ORDEM:
        r = d2_leads[lid]
        marker = f'| {lid} |'
        replacement = f'| {lid} | {r.get("canal_contato","")} | {DATA_HOJE} | | | | | | | | |'
        resultado = resultado.replace(marker, replacement)

    RESULTADO_PATH.write_text(resultado, encoding='utf-8')
    print('Resultado D5 atualizado.')

    print('\n--- Rodando automações ---')
    run('python scripts/follow_up_automacao.py')
    run('python scripts/relatorio_diario_motor_b.py')

    print('\n--- Commit ---')
    run('git add docs/comercial/leads_sao_sebastiao_bertioga.csv docs/comercial/resultado_d5_2026-08-20.md')
    run('git commit -m "feat: publicar Batch D5 — 6 leads enviados e atualizar resultado/CRM 2026-08-20"')

    print('\n=== D5 concluído ===')


if __name__ == '__main__':
    main()
