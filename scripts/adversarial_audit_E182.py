#!/usr/bin/env python3
"""
E.1.8.2 — Adversarial audit para Publication Gate com as 4 correções.
"""
import json
import sys
from pathlib import Path

REPO = Path('C:/Users/Carolina/praia-digital')
TMP_DIR = REPO / 'docs' / 'seo' / 'tmp_adversarial'
TMP_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(REPO / 'scripts' / 'orchestrator' / 'modules'))
from publication_gate import validate_article

RESULTS_FILE = REPO / 'docs' / 'seo' / 'adversarial_gate_E182_results.jsonl'

A = 'placeholder_variations'
B = 'generic_long_text'
C = 'artificially_expanded'
D = 'artificial_h2'
E = 'artificial_internal_link'
F = 'full_metadata_degraded'
G = 'distributed_repetition'
H = 'boundary_cases'
I = 'legitimate_short'
J = 'legitimate_full'
L = 'lorem_ipsum'
K = 'gibberish'
M = 'low_specificity'
N = 'combinations'


def make_html(title, meta, slug, h1, body_content, add_internal_link=False):
    internal = ''
    if add_internal_link:
        internal = '<a href="/blog/artigo-completo.html">Leia mais</a>'
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
{internal}
</body>
</html>"""


def run_case(case_id, category, description, html, expected_block):
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
    }


def main():
    results = []

    # A: Placeholder variations
    base = "<h2>Introdução</h2><p>{text}</p>"
    results.append(run_case('A1', A, 'Exact placeholder', make_html('P','M','p1','P', base.format(text='Conteúdo completo em breve. Para decisões rápidas, use nossas ferramentas de inteligência imobiliária.')), True))
    results.append(run_case('A2', A, 'Uppercase placeholder', make_html('P','M','p2','P', base.format(text='CONTEÚDO COMPLETO EM BREVE.')), True))
    results.append(run_case('A3', A, 'Extra spaces', make_html('P','M','p3','P', base.format(text='Conteúdo  completo   em   breve!')), True))
    results.append(run_case('A4', A, 'Synonym substitution', make_html('P','M','p4','P', base.format(text='Conteúdo completo em breve. Para decisões rápidas, utilize nossas ferramentas de inteligência imobiliária.')), True))
    results.append(run_case('A5', A, 'Tag inside placeholder', make_html('P','M','p5','P', base.format(text='Conteúdo <b>completo</b> em breve.')), True))
    results.append(run_case('A6', A, 'Different punctuation', make_html('P','M','p6','P', base.format(text='Conteúdo completo em breve, para decisões rápidas, use nossas ferramentas.')), True))

    # B: Generic long text
    generic_long = "<h2>Gestão</h2><p>" + ("A locação de temporada exige gestão profissional de reservas, limpeza, regras de cancelamento e atendimento ao hóspede. " * 25) + "</p>"
    results.append(run_case('B1', B, 'Generic long >120 words', make_html('G','M','g1','G', generic_long), True))

    # C: Lorem ipsum expanded
    lorem_content = (
        "<h2>Tópico A</h2><p>" + ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 15) + "</p>" +
        "<h2>Tópico B</h2><p>" + ("Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " * 15) + "</p>" +
        "<h2>Tópico C</h2><p>" + ("Ut enim ad minim veniam, quis nostrud exercitation ullamco. " * 15) + "</p>"
    )
    results.append(run_case('C1', C, 'Lorem ipsum expanded', make_html('L','M','l1','L', lorem_content), True))

    # D: Artificial H2s
    artificial_h2 = "<h2>Introdução</h2><p>Texto curto.</p><h2>Desenvolvimento</h2><p>Texto curto.</p><h2>Conclusão</h2><p>Texto curto.</p>"
    results.append(run_case('D1', D, '3 generic H2s', make_html('H','M','h1','H', artificial_h2), True))

    # E: Irrelevant internal link (legitimate content + 2 H2 + link)
    link_content = (
        "<h2>Seção Principal</h2><p>" + ("Conteúdo legítimo e relevante sobre o mercado imobiliário no litoral paulista. " * 20) + "</p>" +
        "<h2>Segunda Seção</h2><p>" + ("Análise de dados locais e tendências de captação. " * 20) + "</p>"
    )
    results.append(run_case('E1', E, 'Irrelevant internal link', make_html('L','M','lk1','L', link_content, add_internal_link=True), False))

    # F: Full metadata + degraded content
    degraded_structured = (
        "<h2>Seção Um</h2><p>" + ("Conteúdo genérico sem informação específica. " * 20) + "</p>" +
        "<h2>Seção Dois</h2><p>" + ("Mais conteúdo genérico preenchendo estrutura. " * 20) + "</p>"
    )
    results.append(run_case('F1', F, 'Full metadata + generic', make_html('M','Meta description coerente e completa sobre o tema.','mf1','M', degraded_structured), True))

    # G: Distributed repetition
    distributed = (
        "<h2>Parte Um</h2><p>" + "Aluguel de temporada exige gestão profissional. " * 10 + "</p>" +
        "<h2>Parte Dois</h2><p>" + "Imóvel no litoral exige avaliação cuidadosa. " * 10 + "</p>" +
        "<h2>Parte Três</h2><p>" + "Dica reduz risco quando bem aplicada. " * 10 + "</p>"
    )
    results.append(run_case('G1', G, 'Distributed repetition', make_html('D','M','dr1','D', distributed), True))

    # H: Boundary cases
    # H1: word count - fixed 2 H2s + link, vary only word count
    for count, expected in [(119, True), (120, False), (121, False)]:
        content = (
            f"<h2>Primeira</h2><p>{'palavra ' * count}</p>" +
            f"<h2>Segunda</h2><p>{'palavra ' * count}</p>"
        )
        results.append(run_case(f'H1_{count}w', H, f'{count} words', make_html('B','M',f'hw{count}','B', content, add_internal_link=True), expected))

    # H2: byte size - fixed 2 H2s + link + 120+ words, vary only padding bytes
    for size, expected in [(799, True), (800, False), (801, False)]:
        base_text = 'palavra ' * 20
        base_bytes = len(base_text.encode('utf-8'))
        padding_needed = max(0, size - base_bytes)
        content = (
            f"<h2>Primeira</h2><p>{base_text}{'x' * padding_needed}</p>" +
            f"<h2>Segunda</h2><p>{base_text}{'x' * padding_needed}</p>"
        )
        results.append(run_case(f'H2_{size}b', H, f'{size} bytes', make_html('B','M',f'hb{size}','B', content, add_internal_link=True), expected))

    # H3: H2 count boundaries
    content_1h2 = "<h2>Única</h2><p>" + ("Texto suficiente com palavras válidas e conteúdo desenvolvido sobre o tema editorial. " * 20) + "</p>"
    results.append(run_case('H3_1h2', H, '1 H2 boundary', make_html('B','M','h2one','B', content_1h2, add_internal_link=True), True))

    content_2h2 = (
        "<h2>Primeira</h2><p>" + ("Texto suficiente com palavras válidas e conteúdo desenvolvido sobre o tema. " * 15) + "</p>" +
        "<h2>Segunda</h2><p>" + ("Mais conteúdo válido sobre o tema específico. " * 15) + "</p>"
    )
    results.append(run_case('H3_2h2', H, '2 H2 boundary', make_html('B','M','h2two','B', content_2h2, add_internal_link=True), False))

    # I: Legitimate short near boundary
    legitimate_short = "<h2>Contexto</h2><p>" + ("Palavra legítima e específica sobre o tema. " * 25) + "</p>"
    results.append(run_case('I1', I, 'Legitimate short near boundary', make_html('L','Meta description coerente e específica.','ls1','L', legitimate_short, add_internal_link=True), False))

    # J: Legitimate full
    legitimate_full = (
        "<h2>Introdução</h2><p>" + ("Este artigo oferece uma análise específica sobre oportunidades no litoral paulista, combinando dados de mercado, exemplos práticos e recomendações direcionadas para corretores e proprietários. " * 15) + "</p>" +
        "<h2>Análise</h2><p>" + ("Os dados locais mostram variação por cidade, temporada e perfil de imóvel, exigindo estratégias distintas para captação, avaliação e negociação. " * 15) + "</p>" +
        "<h2>Conclusão</h2><p>" + ("Profissionais que combinam presença digital, atendimento estruturado e conhecimento local obtêm melhores resultados em vendas e locação. " * 15) + "</p>"
    )
    results.append(run_case('J1', J, 'Legitimate full article', make_html('G','Guia completo de vendas no litoral paulista: análise de mercado, captação, avaliação e fechamento.','gf1','Guia completo de vendas no litoral paulista', legitimate_full, add_internal_link=True), False))

    # L: Lorem ipsum tests
    # L1: Short lorem ipsum
    lorem_short = "<h2>Intro</h2><p>Lorem ipsum dolor sit amet.</p><p>Sed do eiusmod tempor.</p><p>Ut enim ad minim.</p>"
    results.append(run_case('L1', L, 'Short lorem ipsum', make_html('L','M','ls1','L', lorem_short, add_internal_link=True), True))

    # L2: Lorem ipsum with case variations
    lorem_case = "<h2>Intro</h2><p>LOREM IPSUM DOLOR SIT AMEN.</p><p>SED DO EIUSMOD TEMPOR.</p><p>UT ENIM AD MINIM.</p>"
    results.append(run_case('L2', L, 'Uppercase lorem ipsum', make_html('L','M','ls2','L', lorem_case, add_internal_link=True), True))

    # L3: Lorem ipsum distributed across sections
    lorem_distributed = (
        "<h2>Seção 1</h2><p>Lorem ipsum dolor sit amet, consectetur.</p>" +
        "<h2>Seção 2</h2><p>Sed do eiusmod tempor incididunt.</p>" +
        "<h2>Seção 3</h2><p>Ut enim ad minim veniam.</p>"
    )
    results.append(run_case('L3', L, 'Distributed lorem ipsum', make_html('L','M','ls3','L', lorem_distributed, add_internal_link=True), True))

    # L4: Legitimate content with incidental lorem words
    legit_with_lorem = "<h2>Seção</h2><p>" + ("Este artigo lorem descreve oportunidades reais no litoral. " * 15) + "</p>"
    results.append(run_case('L4', L, 'Legit with incidental lorem words', make_html('L','M','ls4','L', legit_with_lorem, add_internal_link=True), False))

    # K: Gibberish tests
    # K1: Repeated chars (gibberish)
    gibberish_chars = "<h2>Intro</h2><p>aaaaaaa bbbbbbbb cccccccc dddddddd.</p><p>eeeeeeeee fffffffffgggggggg.</p>"
    results.append(run_case('K1', K, 'Repeated chars gibberish', make_html('G','M','gk1','G', gibberish_chars, add_internal_link=True), True))

    # K2: Non-latin chars
    nonlatin = "<h2>Intro</h2><p>Páеѕа genuína com conteúdo real e específico sobre imóveis.</p>"
    results.append(run_case('K2', K, 'Non-latin chars (legitimate)', make_html('G','M','gk2','G', nonlatin, add_internal_link=True), False))

    # K3: Keyboard walk pattern
    keyboard = "<h2>Intro</h2><p>qwertyuiopasdfghjklzxcvbnm foi digitado por engano.</p><p>lkjhgfdsaqwertyuiopzxcv.</p>"
    results.append(run_case('K3', K, 'Keyboard walk gibberish', make_html('G','M','gk3','G', keyboard, add_internal_link=True), True))

    # M: Low specificity tests
    # M1: High filler ratio
    filler_text = (
        "<h2>Introdução</h2><p>" +
        ("É importante notar que é possível ajudar você com muitas informações. " * 10) +
        "</p>" +
        "<h2>Análise</h2><p>" +
        ("Muitos profissionais podem ser melhores quando você precisa. " * 10) +
        "</p>"
    )
    results.append(run_case('M1', M, 'High filler ratio', make_html('M','M','ml1','M', filler_text, add_internal_link=True), True))

    # M2: Low lexical diversity
    low_diversity = (
        "<h2>Seção</h2><p>" +
        ("Palavra palavra palavra palavra palavra palavra palavra palavra. " * 15) +
        "</p>" +
        "<h2>Segunda</h2><p>" +
        ("Palavra palavra palavra palavra palavra palavra palavra palavra. " * 15) +
        "</p>"
    )
    results.append(run_case('M2', M, 'Low lexical diversity (repeated)', make_html('L','M','ml2','L', low_diversity, add_internal_link=True), True))

    # M3: Generic sentences
    generic_sentences = (
        "<h2>Seção</h2><p>" +
        ("conteúdo genérico sem informação específica. " * 5) +
        "Mais conteúdo genérico preenchendo estrutura. " * 5 +
        "</p>" +
        "<h2>Segunda</h2><p>" +
        ("Sem informação específica ainda. " * 5) +
        "Conteúdo vazio para preenchimento. " * 5 +
        "</p>"
    )
    results.append(run_case('M3', M, 'Generic sentence patterns', make_html('M','M','ml3','M', generic_sentences, add_internal_link=True), True))

    # M4: Legitimate intro with simple language
    legit_simple = (
        "<h2>Introdução</h2><p>" +
        ("A locação no litoral exige atenção e organização. " * 10) +
        "</p>" +
        "<h2>Dicas</h2><p>" +
        ("Profissionais podem ajudar com planos e acompanhamento. " * 10) +
        "</p>"
    )
    results.append(run_case('M4', M, 'Legitimate intro, simple language', make_html('L','M','ml4','L', legit_simple, add_internal_link=True), False))

    # N: Combinations
    # Combination A: Lorem ipsum + metadata + 2H2 + link
    comb_a = (
        "<h2>Tópico A</h2><p>" + ("Lorem ipsum dolor sit amet consectetur. " * 15) + "</p>" +
        "<h2>Tópico B</h2><p>" + ("Sed do eiusmod tempor incididunt ut. " * 15) + "</p>"
    )
    results.append(run_case('NA1', N, 'CombA: lorem + metadata + 2H2 + link', make_html('G','Meta description coerente sobre o tema.','nab1','G', comb_a, add_internal_link=True), True))

    # Combination B: Generic long + distributed repetition + metadata
    comb_b = (
        "<h2>Parte Um</h2><p>" + ("Aluguel de temporada exige gestão profissional. " * 15) + "</p>" +
        "<h2>Parte Dois</h2><p>" + ("Imóvel no litoral exige avaliação cuidadosa. " * 15) + "</p>" +
        "<h2>Parte Três</h2><p>" + ("Dica reduz risco quando bem aplicada. " * 15) + "</p>"
    )
    results.append(run_case('NB1', N, 'CombB: generic long + distributed rep + metadata', make_html('G','Meta description coerente e completa.','nbb1','G', comb_b), True))

    # Combination C: Low specificity + 2H2 + link
    comb_c = (
        "<h2>Seção</h2><p>" +
        ("É importante notar que pode ajudar você com muitas informações. " * 5) +
        "A locação no litoral exige atenção. " * 5 +
        "</p>" +
        "<h2>Segunda</h2><p>" +
        ("Muitos profissionais podem ser melhores quando você precisa. " * 5) +
        "Profissionais podem ajudar com planos. " * 5 +
        "</p>"
    )
    results.append(run_case('NC1', N, 'CombC: low specificity + 2H2 + link', make_html('G','Meta description coerente.','nbc1','G', comb_c, add_internal_link=True), True))

    # Combination D: Lorem + distributed + structure complete
    comb_d = (
        "<h2>Seção 1</h2><p>" + ("Lorem ipsum dolor sit amet consectetur adipiscing. " * 8) + "</p>" +
        "<h2>Seção 2</h2><p>" + ("Sed do eiusmod tempor incididunt ut labore. " * 8) + "</p>" +
        "<h2>Seção 3</h2><p>" + ("Ut enim ad minim veniam quis nostrud. " * 8) + "</p>"
    )
    results.append(run_case('ND1', N, 'CombD: lorem + distributed + complete structure', make_html('G','Meta descrição coerente.','ndd1','G', comb_d, add_internal_link=True), True))

    # Write results
    with RESULTS_FILE.open('w', encoding='utf-8') as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')

    total = len(results)
    correct = sum(1 for r in results if (not r['passed'] and r['expected_block']) or (r['passed'] and not r['expected_block']))
    fn = [r for r in results if r['passed'] and r['expected_block']]
    fp = [r for r in results if not r['passed'] and not r['expected_block']]

    print(f"Total cases: {total}")
    print(f"Correct: {correct}/{total}")
    print(f"False negatives: {len(fn)}")
    if fn:
        for r in fn:
            print(f"  - {r['case_id']}: {r['description']}")
    print(f"False positives: {len(fp)}")
    if fp:
        for r in fp:
            print(f"  - {r['case_id']}: {r['description']}")
    print(f"\nResults written to: {RESULTS_FILE}")

    for r in results:
        status = 'PASS' if r['passed'] else 'BLOCK'
        match = 'OK' if (r['passed'] and not r['expected_block']) or (not r['passed'] and r['expected_block']) else 'MISMATCH'
        print(f"{r['case_id']}: {status} (expected {'BLOCK' if r['expected_block'] else 'PASS'}) [{match}]")


if __name__ == '__main__':
    main()
