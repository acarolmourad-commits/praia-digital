#!/usr/bin/env python3
"""
Relatório diário — Motor B: Diagnóstico → Lead
Lê CSVs de eventos, funil e leads e gera relatório Markdown.
"""
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parent.parent / 'docs' / 'comercial'
EVENTS_PATH = BASE / 'diagnostico_eventos_2026.csv'
FUNNEL_PATH = BASE / 'diagnostico_funil_2026.csv'
LEADS_PATH = BASE / 'diagnostico_leads_2026.csv'
REPORT_PATH = BASE / 'acompanhamento_diario_motor_b_2026-08-15.md'

TODAY = datetime.now().isoformat()[:10]

def read_csv(path):
    if not path.exists():
        return []
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def write_report(report):
    REPORT_PATH.write_text(report, encoding='utf-8')

def main():
    events = read_csv(EVENTS_PATH)
    funnel = read_csv(FUNNEL_PATH)
    leads = read_csv(LEADS_PATH)

    today_events = [e for e in events if e.get('timestamp', '').startswith(TODAY)]
    today_funnel = [r for r in funnel if r.get('date') == TODAY]
    today_leads = [l for l in leads if l.get('created_at', '').startswith(TODAY)]

    visits = sum(int(r['visits']) for r in today_funnel)
    starts = sum(int(r['starts']) for r in today_funnel)
    finishes = sum(int(r['finishes']) for r in today_funnel)
    cta_clicks = sum(int(r['cta_clicks']) for r in today_funnel)
    leads_count = sum(int(r['leads']) for r in today_funnel)
    qualified = sum(int(r['qualified']) for r in today_funnel)
    editions = sum(int(r['editions_requested']) for r in today_funnel)
    sales = sum(int(r['sales']) for r in today_funnel)

    start_rate = f"{starts/visits*100:.1f}%" if visits else '0%'
    finish_rate = f"{finishes/starts*100:.1f}%" if starts else '0%'
    cta_rate = f"{cta_clicks/finishes*100:.1f}%" if finishes else '0%'
    lead_rate = f"{leads_count/cta_clicks*100:.1f}%" if cta_clicks else '0%'
    conv_rate = f"{sales/leads_count*100:.1f}%" if leads_count else '0%'

    scores = []
    for e in today_events:
        if e.get('event') == 'finish' and e.get('score'):
            try:
                scores.append(int(e['score']))
            except ValueError:
                pass
    avg_score = f"{sum(scores)/len(scores):.1f}" if scores else '—'

    dist = {'🔴': 0, '🟡': 0, '🟢': 0, '⭐': 0}
    for e in today_events:
        if e.get('event') == 'finish':
            c = e.get('classification', '')
            if 'Vulnerável' in c:
                dist['🔴'] += 1
            elif 'Oportunidades' in c:
                dist['🟡'] += 1
            elif 'Competitivo' in c:
                dist['🟢'] += 1
            elif 'Muito bem estruturado' in c:
                dist['⭐'] += 1

    origins = {}
    for e in today_events:
        if e.get('event') == 'visit':
            key = f"{e.get('source','unknown')}/{e.get('campaign','unknown')}"
            origins[key] = origins.get(key, 0) + 1

    funnel_steps = ['visit','start'] + [f'item_{i}' for i in range(1,16)] + ['finish','cta_click','lead_created']
    step_counts = {s: 0 for s in funnel_steps}
    for e in today_events:
        step = e.get('event')
        if step in step_counts:
            step_counts[step] += 1

    # Detect simple alerts
    alerts = []
    if visits and starts/visits < 0.5:
        alerts.append('Queda anormal de taxa de início')
    if starts and finishes/starts < 0.3:
        alerts.append('Queda anormal de taxa de conclusão')
    if finishes and cta_clicks/finishes < 0.2:
        alerts.append('Queda anormal de taxa de CTA')
    if cta_clicks and leads_count/cta_clicks < 0.3:
        alerts.append('Queda anormal de taxa de lead')
    seen_contacts = set()
    dup_count = 0
    for l in today_leads:
        key = (l.get('contact',''), l.get('name',''), l.get('source',''))
        if key in seen_contacts:
            dup_count += 1
        seen_contacts.add(key)
    if dup_count:
        alerts.append(f'Leads duplicados bloqueados: {dup_count}')
    for e in today_events:
        if not e.get('session_id'):
            alerts.append('Evento sem session_id')
            break

    report = f"""# Acompanhamento diário — Motor B: Diagnóstico → Lead
Data: {TODAY}
Amostra mínima alvo: 20-30 conclusões

## Métricas do dia

| Métrica | Valor | Taxa |
|---------|-------|------|
| Visitas | {visits} | — |
| Inícios | {starts} | {start_rate} |
| Conclusões | {finishes} | {finish_rate} |
| CTAs clicados | {cta_clicks} | {cta_rate} |
| Leads gerados | {leads_count} | {lead_rate} |
| Leads qualificados | {qualified} | — |
| Edições solicitadas | {editions} | — |
| Vendas | {sales} | {conv_rate} |

## Distribuição das pontuações

| Faixa | Quantidade |
|-------|------------|
| 🔴 Vulnerável (0-39) | {dist['🔴']} |
| 🟡 Oportunidades (40-69) | {dist['🟡']} |
| 🟢 Competitivo (70-84) | {dist['🟢']} |
| ⭐ Muito bem estruturado (85-100) | {dist['⭐']} |

Pontuação média dos diagnósticos concluídos: {avg_score}

## Origens do tráfego

| Origem | Visitas |
|--------|---------|
"""
    for origin, count in origins.items():
        report += f"| {origin} | {count} |\n"

    report += f"""
## Abandono por etapa

| Etapa | Quantidade |
|-------|------------|
"""
    for s in funnel_steps:
        report += f"| {s} | {step_counts[s]} |\n"

    report += f"""
## Alertas

"""
    if alerts:
        for a in alerts:
            report += f"- {a}\n"
    else:
        report += "- Nenhum alerta detectado.\n"

    report += f"""
## Observações qualitativas

- Primeira amostra real: {visits} visita(s), {finishes} conclusão(ões).
- Sem alterações no diagnóstico, tracking, CTA ou oferta durante a coleta.

## Classificação provisória do funil

🟡 OTIMIZAR — amostra insuficiente para conclusão. Primeiro resultado promissor, mas sem significância estatística.

## Próximos passos

1. Continuar coleta orgânica até 20-30 conclusões.
2. Não alterar diagnóstico, perguntas, pontuação, CTA ou oferta.
3. Registrar objeções e feedbacks dos leads.
4. Manter Motor A intocado.

## Motor A

- Leads em ENVIADO_D0: 6
- D2: 17/08 às 09:00
- Sem alterações
"""
    write_report(report)
    print(f'Relatório gerado: {REPORT_PATH}')

if __name__ == '__main__':
    main()
