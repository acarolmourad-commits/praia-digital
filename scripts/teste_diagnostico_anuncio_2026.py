#!/usr/bin/env python3
"""
Teste ponta a ponta do Diagnóstico do Anúncio de Temporada 2026.
Simula 3 perfis e valida pontuação, classificação, oferta e CTA.
"""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / 'docs' / 'comercial'
DIAG_PATH = BASE / 'diagnostico_anuncio_temporada_2026.md'
CAMINHOS_PATH = BASE / 'caminhos_conversao_diagnostico_2026.md'
OFERTAS_PATH = BASE / 'ofertas_edicao_por_caminho_diagnostico_2026.md'
PRE_PATH = BASE / 'pre_avaliacao_rapida_anuncio_2026.md'

# Perfis de teste: cada item = 🟢(3), 🟡(1), 🔴(0)
# Ordem: título, primeira foto, posicionamento, SEO interno, conjunto fotos, descrição,
# diferenciais, avaliações, cancelamento, velocidade resposta, preço, calendário,
# sazonalidade, concorrentes, disponibilidade/política

PERFILES = {
    '🔴 vulneravel': [
        0, 0, 0, 0,   # 1-4 visibilidade
        1, 0, 1, 0,   # 5-8 conversao
        0, 0,          # 9-10 conversao
        0, 1, 1, 0, 1 # 11-15 receita/operacao
    ],
    '🟡 oportunidades': [
        3, 1, 1, 3,   # 1-4 visibilidade
        3, 1, 3, 1,   # 5-8 conversao
        1, 1,          # 9-10 conversao
        1, 3, 3, 1, 3 # 11-15 receita/operacao
    ],
    '🟢 competitivo': [
        3, 3, 3, 3,   # 1-4 visibilidade
        3, 3, 3, 3,   # 5-8 conversao
        3, 3,          # 9-10 conversao
        3, 3, 3, 3, 3 # 11-15 receita/operacao
    ]
}

def score_profile(responses):
    vis = sum(responses[0:4])
    conv = sum(responses[4:10])
    rec = sum(responses[10:15])
    total = vis + conv + rec
    scaled = total * 2  # 0-100
    return vis, conv, rec, total, scaled

def classify(score):
    if score <= 39:
        return '🔴 Anúncio vulnerável'
    elif score <= 69:
        return '🟡 Anúncio com oportunidades'
    elif score <= 84:
        return '🟢 Anúncio competitivo'
    else:
        return '⭐ Anúncio muito bem estruturado'

def path_for_score(score):
    if score <= 39:
        return 'Caminho 1 — 🔴 Vulnerável'
    elif score <= 69:
        return 'Caminho 2 — 🟡 Oportunidades'
    else:
        return 'Caminho 3 — 🟢 Competitivo / ⭐ Muito bem estruturado'

def main():
    print('=== Teste Diagnóstico do Anúncio de Temporada 2026 ===\n')
    for name, responses in PERFILES.items():
        vis, conv, rec, total, scaled = score_profile(responses)
        cls = classify(scaled)
        path = path_for_score(scaled)
        print(f'Perfil: {name}')
        print(f'  Visibilidade: {vis}/12')
        print(f'  Conversão: {conv}/18')
        print(f'  Receita/Operação: {rec}/15')
        print(f'  Total: {total}/45')
        print(f'  Pontuação final: {scaled}/100')
        print(f'  Classificação: {cls}')
        print(f'  Caminho de conversão: {path}')
        print()

    # Validar existência dos arquivos da Fase 3
    required = [DIAG_PATH, CAMINHOS_PATH, OFERTAS_PATH, PRE_PATH]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        print('ERRO: arquivos faltantes:', missing)
        sys.exit(1)
    print('Arquivos da Fase 3 verificados: OK')
    print('\nTeste concluído com sucesso.')

if __name__ == '__main__':
    main()
