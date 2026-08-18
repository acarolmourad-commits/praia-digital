#!/usr/bin/env python3
"""
Adversarial audit of publication_gate.py.
Writes results to a JSONL file to avoid large stdout.
Uses a temp dir inside the repo so relative_to(REPO) works.
"""
import json
import re
import sys
import tempfile
from pathlib import Path

REPO = Path('C:/Users/Carolina/praia-digital')
TEMP_DIR = REPO / 'docs' / 'seo' / 'tmp_adversarial'
TEMP_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(REPO / 'scripts' / 'orchestrator' / 'modules'))
from publication_gate import validate_article

RESULTS_PATH = REPO / 'docs' / 'seo' / 'adversarial_gate_results.jsonl'

CASES = []


def case(tid, typ, char, expected, html, note=''):
    p = TEMP_DIR / f'{tid}.html'
    p.write_text(html, encoding='utf-8')
    r = validate_article(p)
    CASES.append({
        'id': tid,
        'type': typ,
        'characteristic': char,
        'expected': expected,
        'result': 'PASS' if r['pass'] else 'BLOCK',
        'blocked': r['blocked'],
        'issues': r.get('issues', []),
        'words': r.get('words'),
        'size': r.get('size'),
        'h2_count': r.get('h2_count'),
        'internal_links': r.get('internal_links'),
        'note': note,
    })


BASE_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="https://praia.digital/blog/{slug}.html">
</head>
<body>
<h1>{h1}</h1>
{content}
<a href="https://praia.digital/blog/outro-artigo.html">link interno</a>
</body>
</html>"""


# A: placeholder variations
A_CONTENT = "<h2>Intro</h2><p>Conteúdo completo em breve. Para decisões rápidas, use nossas ferramentas.</p>"
case('A1', 'placeholder', 'exata original', 'BLOCK', BASE_HTML.format(
    title='Placeholder', meta='...', slug='ph1', h1='Placeholder', content=A_CONTENT), 'string exata')
case('A2', 'placeholder', 'caixa alta', 'BLOCK', BASE_HTML.format(
    title='Placeholder', meta='...', slug='ph2', h1='Placeholder', content="<h2>Intro</h2><p>CONTEÚDO COMPLETO EM BREVE.</p>"), 'caixa alta')
case('A3', 'placeholder', 'espaços/pontuação', 'BLOCK', BASE_HTML.format(
    title='Placeholder', meta='...', slug='ph3', h1='Placeholder', content="<h2>Intro</h2><p>Conteúdo completo  em  breve!</p>"), 'espaços extras e exclamação')
case('A4', 'placeholder', 'sinônimo próximo', 'BLOCK', BASE_HTML.format(
    title='Placeholder', meta='...', slug='ph4', h1='Placeholder', content="<h2>Intro</h2><p>Conteúdo completo em breve. Para decisões rápidas, utilize nossas ferramentas de inteligência imobiliária.</p>"), 'sinônimo "utilize"')
case('A5', 'placeholder', 'capitalização mista', 'BLOCK', BASE_HTML.format(
    title='Placeholder', meta='...', slug='ph5', h1='Placeholder', content="<h2>Intro</h2><p>Conteúdo Completo Em Breve.</p>"), 'capitalização mista')
case('A6', 'placeholder', 'tag no meio', 'BLOCK', BASE_HTML.format(
    title='Placeholder', meta='...', slug='ph6', h1='Placeholder', content="<h2>Intro</h2><p>Conteúdo <b>completo</b> em breve.</p>"), 'tag no meio')


# B: generic text above 120 words
generic_long = (
    "<h2>Gestão</h2><p>" +
    "A locação de temporada exige gestão profissional de reservas, limpeza, regras de cancelamento e atendimento ao hóspede. " * 20 +
    "</p>"
)
case('B1', 'generic_long', 'repetição longa >120 palavras', 'BLOCK', BASE_HTML.format(
    title='Genérico', meta='...', slug='gb1', h1='Genérico', content=generic_long), 'repetição longa')


# C: artificially expanded but degraded
c_content = (
    "<h2>Tópico A</h2><p>" + ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " * 10) + "</p>" +
    "<h2>Tópico B</h2><p>" + ("Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. " * 10) + "</p>" +
    "<h2>Tópico C</h2><p>" + ("Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. " * 10) + "</p>"
)
case('C1', 'artificial_expand', 'lorem >120 palavras, 3H2, 800+ bytes', 'BLOCK', BASE_HTML.format(
    title='Artificial', meta='...', slug='ce1', h1='Artificial', content=c_content), 'lorem expandido')


# D: artificial H2s
d_content = (
    "<h2>Introdução</h2><p>Texto.</p>" +
    "<h2>Desenvolvimento</h2><p>Texto.</p>" +
    "<h2>Conclusão</h2><p>Texto.</p>"
)
case('D1', 'artificial_h2', '3 H2 genéricos', 'BLOCK', BASE_HTML.format(
    title='H2 Art', meta='...', slug='ha1', h1='H2 Art', content=d_content), 'H2 genéricos')


# E: artificial internal link
e_content = "<h2>Sec</h2><p>" + ("Texto mínimo com mais palavras para passar threshold. " * 20) + "</p>"
case('E1', 'artificial_link', 'link irrelevante', 'PASS', BASE_HTML.format(
    title='Link', meta='...', slug='lk1', h1='Link', content=e_content), 'link irrelevante satisfaz regra')


# F: full metadata + degraded content
f_content = (
    "<h2>Seção Um</h2><p>" + ("Conteúdo genérico mas com metadata completa. " * 20) + "</p>" +
    "<h2>Seção Dois</h2><p>" + ("Mais conteúdo genérico preenchendo estrutura. " * 20) + "</p>"
)
case('F1', 'metadata_full', 'metadata completa, conteúdo genérico', 'BLOCK', BASE_HTML.format(
    title='Metadata Full', meta='Meta description válida e coerente com o artigo.', slug='mf1', h1='Metadata Full', content=f_content), 'metadata ok, conteúdo genérico')


# G: distributed repetition
g_content = (
    "<h2>Parte Um</h2><p>" +
    "Aluguel de temporada exige gestão profissional. " * 10 +
    "</p><h2>Parte Dois</h2><p>" +
    "Imóvel no litoral exige avaliação cuidadosa. " * 10 +
    "</p><h2>Parte Três</h2><p>" +
    "Dica reduz risco quando bem aplicada. " * 10 +
    "</p>"
)
case('G1', 'distributed_repeat', 'repetição distribuída', 'BLOCK', BASE_HTML.format(
    title='Distrib', meta='...', slug='dr1', h1='Distrib', content=g_content), 'padrões distribuídos')


# H: boundary tests
h_base = "<h2>Sec</h2><p>{words}</p>"
for words, expected in [(119, 'BLOCK'), (120, 'PASS'), (121, 'PASS')]:
    wtext = 'palavra ' * words
    case(f'H1_{words}w', 'boundary', f'{words} palavras', expected, BASE_HTML.format(
        title='Boundary', meta='...', slug=f'hw{words}', h1='Boundary', content=h_base.format(words=wtext)), f'{words} palavras')

h_base_bytes = "<h2>Sec</h2><p>{chars}</p>"
for size, expected in [(799, 'BLOCK'), (800, 'PASS'), (801, 'PASS')]:
    ctext = 'x' * size
    case(f'H2_{size}b', 'boundary', f'{size} bytes', expected, BASE_HTML.format(
        title='Boundary', meta='...', slug=f'hb{size}', h1='Boundary', content=h_base_bytes.format(chars=ctext)), f'{size} bytes')

# I: legitimate short
i_content = "<h2>Contexto</h2><p>" + ("Palavra legítima e específica sobre o tema. " * 25) + "</p>"
case('I1', 'legitimate_short', 'conteúdo legítimo próximo do limite', 'PASS', BASE_HTML.format(
    title='Legítimo Curto', meta='Meta description coerente e específica para o artigo sobre o tema.', slug='lc1', h1='Legítimo Curto', content=i_content), 'conteúdo válido')

# J: legitimate complete
j_content = (
    "<h2>Introdução</h2><p>" +
    ("Este artigo oferece uma análise específica sobre oportunidades no litoral paulista, combinando dados de mercado, exemplos práticos e recomendações direcionadas para corretores e proprietários. " * 15) +
    "</p><h2>Análise</h2><p>" +
    ("Os dados locais mostram variação por cidade, temporada e perfil de imóvel, exigindo estratégias distintas para captação, avaliação e negociação. " * 15) +
    "</p><h2>Conclusão</h2><p>" +
    ("Profissionais que combinam presença digital, atendimento estruturado e conhecimento local obtêm melhores resultados em vendas e locação. " * 15) +
    "</p>"
)
case('J1', 'legitimate_full', 'conteúdo completo e válido', 'PASS', BASE_HTML.format(
    title='Guia completo de vendas no litoral paulista', meta='Guia completo de vendas no litoral paulista: análise de mercado, captação, avaliação e fechamento para corretores e proprietários.',
    slug='gc1', h1='Guia completo de vendas no litoral paulista', content=j_content), 'conteúdo válido')


# K: combined bypass attempts
k_content = (
    "<h2>Gestão</h2><p>" +
    ("Aluguel de temporada exige gestão profissional. " * 30) +
    "</p><h2>Avaliação</h2><p>" +
    ("Imóvel no litoral exige avaliação cuidadosa. " * 30) +
    "</p>"
)
case('K1', 'combined_bypass', 'genérico longo + 2H2 + metadata + link', 'BLOCK', BASE_HTML.format(
    title='Combined', meta='Meta description coerente e válida.', slug='cb1', h1='Combined', content=k_content), 'tentativa combinada 1')

k2_content = (
    "<h2>Seção A</h2><p>" +
    ("Lorem ipsum dolor sit amet. " * 30) +
    "</p><h2>Seção B</h2><p>" +
    ("Consectetur adipiscing elit. " * 30) +
    "</p>"
)
case('K2', 'combined_bypass', 'lorem longo + 2H2 + metadata + link', 'BLOCK', BASE_HTML.format(
    title='Combined 2', meta='Meta description válida e coerente com o artigo.', slug='cb2', h1='Combined 2', content=k2_content), 'tentativa combinada 2')

k3_content = (
    "<h2>Tópico</h2><p>" +
    ("Palavra " * 200) +
    "</p><h2>Outro</h2><p>" +
    ("Palavra " * 200) +
    "</p>"
)
case('K3', 'combined_bypass', 'palavras repetidas + 2H2 + metadata + link', 'BLOCK', BASE_HTML.format(
    title='Combined 3', meta='Meta description válida e coerente.', slug='cb3', h1='Combined 3', content=k3_content), 'tentativa combinada 3')

k4_content = (
    "<h2>Intro</h2><p>" +
    ("Aluguel de temporada exige gestão. " * 20) +
    " Conteúdo completo em breve variante. " * 20 +
    "</p><h2>Meio</h2><p>" +
    ("Imóvel no litoral exige avaliação. " * 20) +
    "</p>"
)
case('K4', 'combined_bypass', 'genérico + placeholder variante + 2H2', 'BLOCK', BASE_HTML.format(
    title='Combined 4', meta='Meta description válida.', slug='cb4', h1='Combined 4', content=k4_content), 'tentativa combinada 4')

k5_content = (
    "<h2>A</h2><p>" +
    ("Aluguel de temporada exige gestão profissional de reservas. " * 25) +
    "</p><h2>B</h2><p>" +
    ("Imóvel no litoral investimento imóvel usado exige avaliação. " * 25) +
    "</p><h2>C</h2><p>" +
    ("Investimento exige inspeção antes da decisão. " * 25) +
    "</p>"
)
case('K5', 'combined_bypass', '3 padrões genéricos diferentes + 3H2', 'BLOCK', BASE_HTML.format(
    title='Combined 5', meta='Meta description válida.', slug='cb5', h1='Combined 5', content=k5_content), 'tentativa combinada 5')


with RESULTS_PATH.open('w', encoding='utf-8') as f:
    for c in CASES:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f'WROTE {len(CASES)} cases to {RESULTS_PATH}')

blocked = sum(1 for c in CASES if c['blocked'])
passed = sum(1 for c in CASES if not c['blocked'])
print(f'Blocked: {blocked}, Passed: {passed}')
for c in CASES:
    status = 'BLOCK' if c['blocked'] else 'PASS'
    print(f"{c['id']}: {status} ({c['type']}) — {c['note']}")
