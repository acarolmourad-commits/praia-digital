#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de follow-ups WhatsApp-first por perfil de lead.
Gera templates HTML prontos para copiar e enviar pelo WhatsApp.
"""

import os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'docs/sales/followup-whatsapp-perfis-praia-digital.html')


def build():
    today = datetime.now().strftime('%d/%m/%Y %H:%M')
    profiles = {
        'quente': {
            'label': 'Lead quente',
            'cta': 'Agendar demo de 15min',
            'text': 'Olá, [nome]! Vi que você tem interesse em [dor]. Posso mostrar em 15 minutos como a Praia Digital resolve isso para a [imobiliaria]. Qual horário fica melhor: amanhã, quarta ou quinta?'
        },
        'morno': {
            'label': 'Lead morno',
            'cta': 'Enviar proposta comercial',
            'text': 'Olá, [nome]! Lembrete rápido: o piloto de 14 dias sem custo continua disponível para a [imobiliaria]. Quer que eu envie a proposta comercial?'
        },
        'frio': {
            'label': 'Lead frio',
            'cta': 'Follow-up curto em 7d',
            'text': 'Olá, [nome]! Enquanto isso, posso enviar um checklist de captação gratuito para a [imobiliaria]? Sem compromisso.'
        },
        'silencioso': {
            'label': 'Lead silencioso',
            'cta': 'Pergunta de baixo esforço',
            'text': 'Olá, [nome]? Tudo bem? Ainda faz sentido para você? Se sim, responda com 1 dos horários: amanhã, quarta ou quinta, 15min.'
        }
    }

    lines = ['<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><title>Follow-ups WhatsApp por Perfil</title>']
    lines.append('<style>body{font-family:Arial,sans-serif;background:#f6f8fb;color:#222;margin:0;padding:20px}')
    lines.append('.card{background:#fff;border-radius:10px;padding:20px;max-width:900px;margin:0 auto 20px;box-shadow:0 2px 8px rgba(0,0,0,.08)}')
    lines.append('h1{font-size:22px;margin:0 0 12px}h2{font-size:16px;margin:18px 0 8px}')
    lines.append('pre{background:#f1f3f6;padding:14px;border-radius:8px;overflow:auto;white-space:pre-wrap;font-size:14px}')
    lines.append('</style></head><body>')
    lines.append(f'<div class="card"><h1>Follow-ups WhatsApp por Perfil</h1><p>Gerado em {today}</p>')

    for key, p in profiles.items():
        lines.append(f'<h2>{p["label"]}</h2>')
        lines.append(f'<pre>{p["text"]}</pre>')
        lines.append(f'<p><strong>CTA sugerido:</strong> {p["cta"]}</p>')

    lines.append('</div></body></html>')
    return '\n'.join(lines)


def main():
    html = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Templates gerados: {OUT}')


if __name__ == '__main__':
    main()
