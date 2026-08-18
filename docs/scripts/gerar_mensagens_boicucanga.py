#!/usr/bin/env python3
"""
Gerador de mensagens personalizadas — Frente Boiçucanga
Saída: docs/comercial/mensagens_boicucanga_prontas.md
"""
import csv
from pathlib import Path
from datetime import date

BASE = Path(__file__).resolve().parent.parent.parent / 'docs' / 'comercial'
LEADS_PATH = BASE / 'leads_boicucanga_classificados.csv'
OUT_PATH = BASE / 'mensagens_boicucanga_prontas.md'

MSG_VENDA = "Vi seu imóvel em Boiçucanga. Pelo perfil da propriedade, acredito que ele possa ter potencial para temporada enquanto permanece disponível para venda. A Praia Digital trabalha com estruturação e administração de anúncios de temporada. Posso fazer uma avaliação rápida do potencial do imóvel e te mostrar como funcionaria?"
MSG_AIRBNB = "Vi seu anúncio em Boiçucanga. Acho que dá para aumentar a conversão com ajustes no título, fotos e descrição. Posso fazer uma avaliação rápida e te mostrar 2-4 oportunidades concretas?"
MSG_FLAT = "Vi seu flat em Boiçucanga. Ele pode funcionar bem para temporada, especialmente para estadias curtas. Posso fazer uma avaliação rápida e te mostrar como funcionaria?"
MSG_MONITORAMENTO = "Acompanhando seu imóvel em Boiçucanga. Quando quiser avaliar potencial para temporada, podemos conversar."


def gerar():
    rows = []
    if not LEADS_PATH.exists():
        print(f'Arquivo não encontrado: {LEADS_PATH}')
        return
    with LEADS_PATH.open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    linhas = [f'# Mensagens personalizadas — Boiçucanga\nData: {date.today().isoformat()}\n']
    for i, r in enumerate(rows, 1):
        titulo = r.get('titulo', '')
        url = r.get('url', '')
        classificacao = r.get('classificacao', '')
        segmento = r.get('segmento', '')
        oferta = r.get('oferta_recomendada', '')
        if classificacao == 'A':
            prioridade_msg = 'CONTATAR PRIMEIRO'
        elif classificacao == 'B':
            prioridade_msg = 'CONTATAR EM SEGUNDA'
        else:
            prioridade_msg = 'MONITORAR — não contatar agora'

        if 'airbnb' in segmento.lower() or 'Edição/otimização de anúncio Airbnb' in oferta:
            msg = MSG_AIRBNB
        elif 'flat' in titulo.lower() or 'Flat' in titulo:
            msg = MSG_FLAT
        elif 'monitoramento' in oferta.lower():
            msg = MSG_MONITORAMENTO
        else:
            msg = MSG_VENDA

        linhas.append(f'## {i}. {titulo}')
        linhas.append(f'- Classificação: {classificacao}')
        linhas.append(f'- Segmento: {segmento}')
        linhas.append(f'- Oferta: {oferta}')
        linhas.append(f'- Prioridade: {prioridade_msg}')
        linhas.append(f'- URL: {url}')
        linhas.append(f'- Mensagem sugerida:\n> {msg}\n')

    OUT_PATH.write_text('\n'.join(linhas), encoding='utf-8')
    print(f'Mensagens geradas: {OUT_PATH}')


if __name__ == '__main__':
    gerar()
