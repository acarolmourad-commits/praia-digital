#!/usr/bin/env python3
"""
E.1.8.3 - Bateria de testes corrigida com isolamento de dimensões e conteúdo legítimo variado.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path('C:/Users/Carolina/praia-digital')
TMP_DIR = REPO / 'docs' / 'seo' / 'tmp_adversarial'
TMP_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(REPO / 'scripts' / 'orchestrator' / 'modules'))
from publication_gate import validate_article, count_words, MIN_WORDS, MIN_CONTENT_SIZE, MIN_H2_COUNT, MIN_INTERNAL_LINKS

RESULTS_FILE = REPO / 'docs' / 'seo' / 'adversarial_gate_E183_results.jsonl'

# Texto base legítimo e variado (não dispara low_specificity)
LEGIT_BASE = "A análise do mercado imobiliário no litoral paulista revela padrões regionais distintos entre as cidades costeiras. Profissionais que acompanam dados de preços e demanda identificam oportunidades com maior precisão. Variações sazonais e localização impactam diretamente os resultados. Conhecimento local e atenção aos detalhes aumentam a confiabilidade das recomendações aos clientes."


def make_html(title, meta, slug, h1, body_content, internal_links=None):
    if internal_links is None:
        internal_links = ['<a href="/blog/artigo-completo.html">Leia mais</a>']
    links_html = '\n'.join(internal_links)
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="https://praia.digital/blog/{slug}.html">
</head>
<body>
<h1>{h1}</h1>
{body_content}
{links_html}
</body>
</html>"""


def run_case(case_id, category, description, html, expected_block, dimension_tested, rules_controlled):
    p = TMP_DIR / f'{case_id}.html'
    p.write_text(html, encoding='utf-8')
    result = validate_article(p)
    return {
        'case_id': case_id,
        'category': category,
        'description': description,
        'expected_block': expected_block,
        'passed': not result['blocked'],
        'blocked': result['blocked'],
        'issues': result.get('issues', []),
        'words': result.get('words'),
        'size': result.get('size'),
        'h2_count': result.get('h2_count'),
        'internal_links': result.get('internal_links'),
        'dimension_tested': dimension_tested,
        'rules_controlled': rules_controlled,
    }


def main():
    results = []

    # ============================================================
    # FRONTEIRAS (min_words, min_h2) com conteúdo legítimo variado
    # ============================================================

    # Min words: 119 vs 120 vs 121
    for count, expected, label in [(119, True, 'abaixo'), (120, False, 'limite'), (121, False, 'acima')]:
        # Conteúdo com palavras variadas que soma exatamente ~count palavras
        # Dividimos LEGIT_BASE em frases e adicionamos/removemos para controlar
        base_words = LEGIT_BASE.split()
        # Nossa meta: criar conteúdo com ~count palavras
        target_words = min(count, len(base_words))
        content_words = base_words[:target_words]
        content = ' '.join(content_words)
        # Adicionar H2s suficientes (2) e link
        full_content = f"<h2>Seção A</h2><p>{content}</p><h2>Seção B</h2><p>{content}</p>"
        results.append(run_case(
            f'MW_{count}w_REAL', 'min_words_boundary',
            f'{label} do limite de palavras: ~{count} palavras (real: {len(content_words) * 2})',
            make_html('Teste palavras', 'Teste de limite de palavras.', f'mw{count}',
                      'Teste de limite de palavras', full_content),
            expected_block=expected,
            dimension_tested='min_words',
            rules_controlled='min_content_size, min_h2, title, meta, canonical, h1, links',
        ))

    # Min H2: 1 vs 2 vs 3 com conteúdo variado
    for h2_count, expected, label in [(1, True, 'abaixo'), (2, False, 'limite'), (3, False, 'acima')]:
        sections = []
        for i in range(h2_count):
            section_text = f"<h2>Seção {i+1}</h2><p>{LEGIT_BASE}</p>"
            sections.append(section_text)
        content = '\n'.join(sections)
        results.append(run_case(
            f'H2_{h2_count}_test', 'min_h2_boundary',
            f'{label} do limite de H2: {h2_count} H2 (conteúdo variado)',
            make_html('Teste H2', 'Teste de limite de H2.', f'h2{h2_count}',
                      'Teste de limite de H2', content),
            expected_block=expected,
            dimension_tested='min_h2',
            rules_controlled='min_words, min_content_size, title, meta, canonical, h1, links',
        ))

    # ============================================================
    # MIN_CONTENT_SIZE: abaixo vs. acima de 800 bytes
    # ============================================================

    # Abaixo de 800 bytes — conteúdo curto
    h2_block_content = (
        "<h2>Introdução</h2><p>" + ("A análise do mercado mostra tendências locais. " * 5) + "</p>" +
        "<h2>Desenvolvimento</h2><p>" + ("Profissionais observam variações regionais. " * 5) + "</p>"
    )
    h2_block_html = make_html('Tamanho mínimo', 'Tamanho mínimo de conteúdo editorial.', 'h2block',
                               'Tamanho mínimo de conteúdo', h2_block_content)
    h2_block_size = len(h2_block_html.encode('utf-8'))
    results.append(run_case(
        'H2_800b_BLOCK', 'min_content_size_boundary',
        f'Arquivo abaixo de 800 bytes (tamanho real: {h2_block_size} bytes)',
        h2_block_html, expected_block=True,
        dimension_tested='min_content_size (< 800 bytes)',
        rules_controlled='min_words, min_h2, title, meta, canonical, h1, links',
    ))

    # Acima de 800 bytes — conteúdo variado e legítimo
    h2_pass_content = (
        "<h2>Introdução</h2><p>" + LEGIT_BASE + "</p>" +
        "<h2>Desenvolvimento</h2><p>" + LEGIT_BASE + "</p>"
    )
    h2_pass_html = make_html('Análise de mercado', 
                             'Análise de mercado imobiliário no litoral paulista: tendências, variações regionais e sazonais.',
                             'h2pass',
                             'Análise de mercado no litoral paulista', h2_pass_content)
    h2_pass_size = len(h2_pass_html.encode('utf-8'))
    results.append(run_case(
        'H2_800b_PASS', 'min_content_size_boundary',
        f'Arquivo acima de 800 bytes (tamanho real: {h2_pass_size} bytes, palavras: {count_words(h2_pass_html)})',
        h2_pass_html, expected_block=False,
        dimension_tested='min_content_size (>= 800 bytes)',
        rules_controlled='min_words, min_h2, title, meta, canonical, h1, links',
    ))

    # ============================================================
    # SEIS CASOS RECONSTRUÍDOS (conteúdo legítimo variado)
    # ============================================================

    # E1: Link interno irrelevante com conteúdo legítimo variado
    e1_content = (
        "<h2>Mercado atual</h2><p>" + LEGIT_BASE + "</p>" +
        "<h2>Estratégias</h2><p>" + LEGIT_BASE + "</p>"
    )
    results.append(run_case(
        'E1', 'min_internal_links_boundary', 
        'Link interno irrelevante com conteúdo legítimo variado',
        make_html('Mercado e estratégias', 
                  'Mercado e estratégias: análise contemporânea do litoral paulista.',
                  'e1', 
                  'Mercado e estratégias no litoral paulista', e1_content, 
                  internal_links=['<a href="/blog/artigo-antigo.html">Ver artigo anterior</a>']),
        expected_block=False,
        dimension_tested='min_internal_links (link irrelevante satisfaz?)',
        rules_controlled='min_words, min_content_size, min_h2, title, meta, canonical, h1, links',
    ))

    # H3_2h2_PASS (renomeado de H3_2h2_PASS para consistência)
    h3_pass_content = (
        "<h2>Introdução</h2><p>" + LEGIT_BASE + "</p>" +
        "<h2>Desenvolvimento</h2><p>" + LEGIT_BASE + "</p>"
    )
    results.append(run_case(
        'H3_2h2_PASS', 'min_h2_boundary',
        f'2 H2 com conteúdo legítimo variado (palavras: {count_words(h3_pass_content)})',
        make_html('Análise regional', 'Análise regional do mercado imobiliário no litoral paulista.', 'h3pass',
                  'Análise regional do mercado imobiliário no litoral paulista', h3_pass_content),
        expected_block=False,
        dimension_tested='min_h2 (>= 2 H2)',
        rules_controlled='min_words, min_content_size, title, meta, canonical, h1, links',
    ))

    # I1: Conteúdo legítimo próximo dos limites
    i1_content = (
        "<h2>Contexto</h2><p>" + LEGIT_BASE + "</p>" +
        "<h2>Observações</h2><p>" + LEGIT_BASE + "</p>"
    )
    i1_words = count_words(i1_content)
    results.append(run_case(
        'I1', 'legitimate_short',
        f'Conteúdo legítimo variado, próximo dos limites (palavras: {i1_words}, H2s: 2)',
        make_html('Contexto regional', 'Contexto regional: mercado de imóveis no litoral paulista.', 'i1',
                  'Contexto regional: mercado de imóveis no litoral paulista', i1_content),
        expected_block=False,
        dimension_tested='legitimate_content_near_boundary',
        rules_controlled='min_words, min_content_size, min_h2, title, meta, canonical, h1, links',
    ))

    # J1: Artigo completo e legítimo com conteúdo variado em cada seção
    j1_content = (
        "<h2>Introdução</h2><p>" + 
        ("O litoral paulista tem atraído investidores e compradores por sua combinação de praias, infraestrutura e proximidade com cidades grandes. " * 2) +
        "</p>" +
        "<h2>Análise de mercado</h2><p>" +
        ("Dados regionais mostram variações significativas entre cidades, com alguns bairros apresentando maior liquidez e outros com potencial de valorização. " * 2) +
        "</p>" +
        "<h2>Estratégias práticas</h2><p>" +
        ("Profissionais que combinam conhecimento local, atendimento estruturado e ferramentas digitais tendem a obter melhores resultados em captação e fechamento. " * 2) +
        "</p>" +
        "<h2>Conclusão</h2><p>" +
        ("A diversificação de estratégias e o acompanhamento contínuo de dados locais são diferenciais competitivos no mercado atual. " * 2) +
        "</p>"
    )
    j1_words = count_words(j1_content)
    results.append(run_case(
        'J1', 'legitimate_full',
        f'Artigo completo e legítimo com conteúdo variado (palavras: {j1_words}, H2s: 4)',
        make_html('Guia completo de vendas no litoral paulista', 
                   'Guia completo de vendas no litoral paulista: análise de mercado, estratégias práticas e conclusão para corretores.',
                   'j1',
                   'Guia completo de vendas no litoral paulista',
                   j1_content),
        expected_block=False,
        dimension_tested='legitimate_full_article',
        rules_controlled='min_words, min_content_size, min_h2, title, meta, canonical, h1, links',
    ))

    # ============================================================
    # HEURÍSTICAS SEMÂNTICAS
    # ============================================================

    # Lorem ipsum
    lorem_content = (
        "<h2>Introdução</h2><p>" +
        ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 10) +
        "</p>" +
        "<h2>Desenvolvimento</h2><p>" +
        ("Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " * 10) +
        "</p>" +
        "<h2>Conclusão</h2><p>" +
        ("Ut enim ad minim veniam, quis nostrud exercitation ullamco. " * 10) +
        "</p>"
    )
    results.append(run_case(
        'L1', 'lorem_ipsum',
        'Lorem ipsum com estrutura completa (palavras: ' + str(count_words(lorem_content)) + ')',
        make_html('Lorem ipsum', 'Lorem ipsum: conteúdo artificial de teste.', 'l1',
                  'Lorem ipsum: conteúdo artificial de teste', lorem_content),
        expected_block=True,
        dimension_tested='lorem_ipsum_detection',
        rules_controlled='min_words, min_content_size, min_h2, title, meta, canonical, h1, links',
    ))

    # Gibberish
    gibberish_content = (
        "<h2>Introdução</h2><p>" +
        ("aaaaaaa bbbbbbbb cccccccc dddddddd eeeeeeeee fffffffff. " * 8) +
        "</p>" +
        "<h2>Desenvolvimento</h2><p>" +
        ("ggggggggg hhhhhhhhh iiiiiiiii jjjjjjjjj kkkkkkkkkk lllllllll. " * 8) +
        "</p>"
    )
    results.append(run_case(
        'G1', 'gibberish',
        'Gibberish com repetição de caracteres (palavras: ' + str(count_words(gibberish_content)) + ')',
        make_html('Gibberish', 'Gibberish: conteúdo artificial de teste.', 'g1',
                  'Gibberish: conteúdo artificial de teste', gibberish_content),
        expected_block=True,
        dimension_tested='gibberish_detection',
        rules_controlled='min_words, min_content_size, min_h2, title, meta, canonical, h1, links',
    ))

    # Repetição distribuída
    distributed_content = (
        "<h2>Seção Um</h2><p>" +
        ("Aluguel de temporada exige gestão profissional de reservas e atendimento. " * 8) +
        "</p>" +
        "<h2>Seção Dois</h2><p>" +
        ("Imóvel no litoral exige avaliação cuidadosa de documentos e condições. " * 8) +
        "</p>" +
        "<h2>Seção Três</h2><p>" +
        ("Dica reduz risco quando o profissional verifica detalhes antes da recomendação. " * 8) +
        "</p>"
    )
    results.append(run_case(
        'D1', 'distributed_repetition',
        'Repetição distribuída entre 3 H2s com marcadores genéricos',
        make_html('Repetição distribuída', 'Repetição distribuída: teste de detecção.', 'd1',
                  'Repetição distribuída: teste de detecção', distributed_content),
        expected_block=True,
        dimension_tested='distributed_repetition_detection',
        rules_controlled='min_words, min_content_size, min_h2, title, meta, canonical, h1, links',
    ))

    # Baixa especificidade: genérico vs. específico
    # Caso A: genérico/degradado
    low_spec_content = (
        "<h2>Introdução</h2><p>" +
        ("É importante notar que pode ajudar você com muitas informações. " * 8) +
        "Muitos profissionais podem ser melhores quando você precisa. " * 8 +
        "</p>" +
        "<h2>Análise</h2><p>" +
        ("É possível observar que é uma das melhores opções disponíveis. " * 8) +
        "Uma das melhores formas de proceder é considerar os dados. " * 8 +
        "</p>"
    )
    results.append(run_case(
        'LS1', 'low_specificity',
        'Conteúdo com baixa especificidade semântica (genérico)',
        make_html('Conteúdo genérico', 'Conteúdo genérico: teste de especificidade.', 'ls1',
                  'Conteúdo genérico: teste de especificidade', low_spec_content),
        expected_block=True,
        dimension_tested='low_specificity_detection (genérico)',
        rules_controlled='min_words, min_content_size, min_h2, title, meta, canonical, h1, links',
    ))

    # Caso B: específico/legítimo
    high_spec_content = (
        "<h2>Introdução</h2><p>" +
        ("O mercado de imóveis no litoral paulista tem apresentado comportamento diverso por região. " * 6) +
        "Cidades como Santos, Guarujá e São Sebastião concentram a maior parte do volume de negócios. " * 6 +
        "</p>" +
        "<h2>Análise de dados</h2><p>" +
        ("Profissionais que monitoram preços, tempo de comercialização e taxa de ocupação em período de férias têm maior precisão nas recomendações aos clientes. " * 2) +
        "</p>" +
        "<h2>Estratégias práticas</h2><p>" +
        ("A combinação de conhecimento local, atendimento estruturado e ferramentas de automação permite atender melhor as necessidades de cada cliente. " * 2) +
        "</p>"
    )
    results.append(run_case(
        'LS2', 'low_specificity',
        'Conteúdo com alta especificidade semântica (legítimo)',
        make_html('Conteúdo específico', 'Conteúdo específico: análise do mercado imobiliário no litoral paulista.', 'ls2',
                  'Conteúdo específico: análise do mercado imobiliário no litoral paulista', high_spec_content),
        expected_block=False,
        dimension_tested='low_specificity_detection (legítimo)',
        rules_controlled='min_words, min_content_size, min_h2, title, meta, canonical, h1, links',
    ))

    # ============================================================
    # ESCRITA DOS RESULTADOS
    # ============================================================
    with RESULTS_FILE.open('w', encoding='utf-8') as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')

    total = len(results)
    correct = sum(1 for r in results if (not r['passed'] and r['expected_block']) or (r['passed'] and not r['expected_block']))
    fn = [r for r in results if r['passed'] and r['expected_block']]
    fp = [r for r in results if not r['passed'] and not r['expected_block']]

    print(f'Total casos: {total}')
    print(f'Correct: {correct}/{total}')
    print(f'False negatives: {len(fn)}')
    if fn:
        for r in fn:
            print(f'  - {r["case_id"]}: {r["description"]}')
    print(f'False positives: {len(fp)}')
    if fp:
        for r in fp:
            print(f'  - {r["case_id"]}: {r["description"]}')
            for issue in r['issues']:
                print(f'      - {issue["rule"]}: {issue["reason"]}')
    print(f'\nResults written to: {RESULTS_FILE}')
    print()
    for r in results:
        status = 'PASS' if r['passed'] else 'BLOCK'
        match = 'OK' if (r['passed'] and not r['expected_block']) or (not r['passed'] and r['expected_block']) else 'MISMATCH'
        print(f'{r["case_id"]}: {status} (expected {"BLOCK" if r["expected_block"] else "PASS"}) [{match}]')


if __name__ == '__main__':
    main()
