#!/usr/bin/env python3
"""
Análise pós-D2 — Motor A
Uso: python scripts/analise_pos_d2_2026-08-17.py
Executa após D2 e gera relatório consolidado.
"""

import csv
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = Path('C:/Users/Carolina/praia-digital')
LEADS_PATH = REPO / 'docs/comercial/leads_sao_sebastiao_bertioga.csv'
RESULTADO_PATH = REPO / 'docs/comercial/resultado_d2_2026-08-17.md'
ANALISE_PATH = REPO / 'docs/comercial/analise_pos_d2_2026-08-17.md'
ORDEM = ['9', '11', '14', '15', '27', '29']


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
    print('=== Análise pós-D2 — Motor A ===')
    print(f'Data/hora: {now.isoformat()}')

    with LEADS_PATH.open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    d2_leads = [r for r in rows if r.get('status') == 'ENVIADO_D2' and r.get('d2_enviado_em') == '2026-08-17']
    print(f'Leads ENVIADO_D2: {len(d2_leads)}')

    respostas = [r for r in d2_leads if r.get('resposta')]
    sem_resposta = [r for r in d2_leads if not r.get('resposta')]

    resposta_pct = f"{(len(respostas)/len(d2_leads))*100:.1f}%" if d2_leads else "N/A (D2 não executado)"

    analysis = f'''# Análise pós-D2 — Motor A
Data: 2026-08-17
Gerado em: {now.isoformat()}

## Métricas
- Leads enviados D2: {len(d2_leads)}
- Respostas: {len(respostas)}
- Sem resposta: {len(sem_resposta)}
- Taxa de resposta: {resposta_pct}

## Respostas
'''

    if respostas:
        for r in respostas:
            analysis += f'- Lead {r.get("lead_id")}: {r.get("tipo_resposta", "N/A")} | {r.get("servico_interesse", "N/A")} | Valor: {r.get("valor_potencial", "N/A")}\n'
    else:
        analysis += 'Nenhuma resposta registrada.\n'

    analysis += '''
## Sem resposta
'''
    if sem_resposta:
        for r in sem_resposta:
            analysis += f'- Lead {r.get("lead_id")} | Canal: {r.get("canal_contato", "N/A")} | Cidade: {r.get("city", "N/A")}\n'
    else:
        analysis += 'Todos os leads responderam.\n'

    analysis += '''
## Próximos passos
'''
    if sem_resposta:
        analysis += '- [ ] Preparar D5 para 20/08\n'
        analysis += '- [ ] Executar D5 se nenhuma resposta até lá\n'
    else:
        analysis += '- [ ] Processar respostas e handoffs\n'

    analysis += '- [ ] Rodar follow_up_automacao.py\n'
    analysis += '- [ ] Rodar relatorio_diario_motor_b.py\n'
    analysis += '- [ ] Commit com resultados\n'

    ANALISE_PATH.write_text(analysis, encoding='utf-8')
    print(f'\nAnálise salva em: {ANALISE_PATH}')

    print('\n--- Rodando automações ---')
    run('python scripts/follow_up_automacao.py')
    run('python scripts/relatorio_diario_motor_b.py')

    print('\n=== Análise concluída ===')


if __name__ == '__main__':
    main()
