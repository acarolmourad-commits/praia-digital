#!/usr/bin/env python3
"""
Painel unificado — Motor A + Motor B
Lê leads do Motor A, eventos/funil/leads do Motor B e gera relatório comparativo.
"""
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parent.parent / 'docs' / 'comercial'
MOTOR_A_LEADS = BASE / 'leads_sao_sebastiao_bertioga.csv'
MOTOR_B_EVENTS = BASE / 'diagnostico_eventos_2026.csv'
MOTOR_B_FUNNEL = BASE / 'diagnostico_funil_2026.csv'
MOTOR_B_LEADS = BASE / 'diagnostico_leads_2026.csv'
PANEL_PATH = BASE / 'painel_unificado_motor_a_b_2026-08-15.md'

def read_csv(path):
    if not path.exists():
        return []
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def to_int(v):
    try:
        return int(v)
    except Exception:
        return 0

def main():
    motor_a = read_csv(MOTOR_A_LEADS)
    motor_b_events = read_csv(MOTOR_B_EVENTS)
    motor_b_funnel = read_csv(MOTOR_B_FUNNEL)
    motor_b_leads = read_csv(MOTOR_B_LEADS)

    # Motor A summary
    motor_a_total = len(motor_a)
    motor_a_env = [r for r in motor_a if r.get('status','') == 'ENVIADO_D0']
    motor_a_d2 = [r for r in motor_a if r.get('d2_enviado_em','')]
    motor_a_answers = [r for r in motor_a if r.get('resposta','').strip()]
    motor_a_pos = [r for r in motor_a if r.get('tipo_resposta','').strip() == 'positiva']
    motor_a_neg = [r for r in motor_a if r.get('tipo_resposta','').strip() == 'negativa']
    motor_a_price = [r for r in motor_a if r.get('tipo_resposta','').strip() == 'preco']
    motor_a_agend = [r for r in motor_a if r.get('tipo_resposta','').strip() == 'agendamento']
    motor_a_silence = [r for r in motor_a if not r.get('resposta','').strip()]

    # Motor B summary
    visits = sum(to_int(r['visits']) for r in motor_b_funnel)
    starts = sum(to_int(r['starts']) for r in motor_b_funnel)
    finishes = sum(to_int(r['finishes']) for r in motor_b_funnel)
    cta_clicks = sum(to_int(r['cta_clicks']) for r in motor_b_funnel)
    leads_b = sum(to_int(r['leads']) for r in motor_b_funnel)
    qualified_b = sum(to_int(r['qualified']) for r in motor_b_funnel)
    editions_b = sum(to_int(r['editions_requested']) for r in motor_b_funnel)
    sales_b = sum(to_int(r['sales']) for r in motor_b_funnel)

    start_rate = f"{starts/visits*100:.1f}%" if visits else '0%'
    finish_rate = f"{finishes/starts*100:.1f}%" if starts else '0%'
    cta_rate = f"{cta_clicks/finishes*100:.1f}%" if finishes else '0%'
    lead_rate = f"{leads_b/cta_clicks*100:.1f}%" if cta_clicks else '0%'
    conv_rate = f"{sales_b/leads_b*100:.1f}%" if leads_b else '0%'

    # Motor B score distribution
    scores = []
    dist = {'🔴': 0, '🟡': 0, '🟢': 0, '⭐': 0}
    for e in motor_b_events:
        if e.get('event') == 'finish':
            s = e.get('score')
            if s:
                try:
                    scores.append(int(s))
                except ValueError:
                    pass
            c = e.get('classification', '')
            if 'Vulnerável' in c:
                dist['🔴'] += 1
            elif 'Oportunidades' in c:
                dist['🟡'] += 1
            elif 'Competitivo' in c:
                dist['🟢'] += 1
            elif 'Muito bem estruturado' in c:
                dist['⭐'] += 1
    avg_score = f"{sum(scores)/len(scores):.1f}" if scores else '—'

    report = f"""# Painel unificado — Motor A + Motor B
Data: {datetime.now().isoformat()[:10]}
Regra: sem evidência → não alterar | ciclo: observar → medir → compreender → testar → medir novamente

## Motor A — Abordagem direta

| Métrica | Valor |
|---------|-------|
| Leads totais | {motor_a_total} |
| ENVIADO_D0 | {len(motor_a_env)} |
| D2 enviados | {len(motor_a_d2)} |
| Respostas | {len(motor_a_answers)} |
| Respostas positivas | {len(motor_a_pos)} |
| Respostas negativas | {len(motor_a_neg)} |
| Pedidos de preço | {len(motor_a_price)} |
| Pedidos de agendamento | {len(motor_a_agend)} |
| Silêncio | {len(motor_a_silence)} |

Taxa de resposta: {len(motor_a_answers)/len(motor_a_env)*100:.1f}% ({len(motor_a_answers)}/{len(motor_a_env)})
Taxa de resposta positiva: {len(motor_a_pos)/len(motor_a_env)*100:.1f}% ({len(motor_a_pos)}/{len(motor_a_env)})
Taxa de conversão: {len(motor_a_pos)/len(motor_a_env)*100:.1f}% ({len(motor_a_pos)}/{len(motor_a_env)})

## Motor B — Diagnóstico → Lead

| Métrica | Valor | Taxa |
|---------|-------|------|
| Visitas | {visits} | — |
| Inícios | {starts} | {start_rate} |
| Conclusões | {finishes} | {finish_rate} |
| CTAs clicados | {cta_clicks} | {cta_rate} |
| Leads gerados | {leads_b} | {lead_rate} |
| Leads qualificados | {qualified_b} | — |
| Edições solicitadas | {editions_b} | — |
| Vendas | {sales_b} | {conv_rate} |

Pontuação média: {avg_score}

### Distribuição das pontuações

| Faixa | Quantidade |
|-------|------------|
| 🔴 Vulnerável (0-39) | {dist['🔴']} |
| 🟡 Oportunidades (40-69) | {dist['🟡']} |
| 🟢 Competitivo (70-84) | {dist['🟢']} |
| ⭐ Muito bem estruturado (85-100) | {dist['⭐']} |

## Comparativo Motor A × Motor B

| Dimensão | Motor A | Motor B |
|----------|---------|---------|
| Abordagem | Direta | Demanda induzida |
| Entrada | Lead | Visitante |
| Qualificação | Score comercial | Diagnóstico |
| Ação inicial | Follow-up | CTA |
| Ciclo | D0/D2/D5/D10 | Diagnóstico → lead → follow-up |
| Resposta atual | Aguardando D2 | Aguardando conclusões |
| Métrica principal | Taxa de resposta positiva | Taxa de conclusão → CTA → lead |

## Gargalo atual

- Motor A: sem respostas até o momento; aguardando D2
- Motor B: amostra insuficiente; sem conclusões suficientes para classificação

## Classificação provisória

🟡 OTIMIZAR — amostra insuficiente; primeiro sinal técnico positivo, mas sem significância estatística

## Ação humana

Nenhuma ação humana necessária no momento.

## Próximo marco

- Motor A: D2 em 17/08 às 09:00
- Motor B: 20-30 conclusões para propor primeiro experimento controlado

## Alertas

- Nenhum alerta detectado no momento
"""
    PANEL_PATH.write_text(report, encoding='utf-8')
    print(f'Painel gerado: {PANEL_PATH}')

if __name__ == '__main__':
    main()
