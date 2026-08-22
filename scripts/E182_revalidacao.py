#!/usr/bin/env python3
"""
E.1.8.2 — Revalidação dos 7 falsos negativos da E.1.8.1 com gate corrigido.
"""
import json
import sys
from pathlib import Path

REPO = Path('C:/Users/Carolina/praia-digital')
TMP_DIR = REPO / 'docs' / 'seo' / 'tmp_adversarial'
TMP_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(REPO / 'scripts' / 'orchestrator' / 'modules'))
from publication_gate import validate_article

# Reconstruir os 7 falsos negativos da E.1.8.1

def run_case(case_id, description, html, expected_block):
    p = TMP_DIR / f'{case_id}.html'
    p.write_text(html, encoding='utf-8')
    result = validate_article(p)
    return {
        'case_id': case_id,
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

    # C1: Lorem ipsum expandido com estrutura completa
    c1_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Lorem ipsum expandido</title>
<meta name="description" content="Lorem ipsum expandido: teste de conteúdo artificial.">
<link rel="canonical" href="https://praia.digital/blog/lorem-expandido.html">
</head>
<body>
<h1>Lorem ipsum expandido</h1>
<h2>Tópico A</h2><p>{"Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 15}</p>
<h2>Tópico B</h2><p>{"Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " * 15}</p>
<h2>Tópico C</h2><p>{"Ut enim ad minim veniam, quis nostrud exercitation ullamco. " * 15}</p>
<a href="/blog/artigo-completo.html">Leia mais</a>
</body>
</html>"""
    results.append(run_case('C1', 'Lorem ipsum expandido com 3 H2 e 530 palavras', c1_html, True))

    # F1: Metadata completa + conteúdo genérico sem informação específica
    f1_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Conteúdo genérico</title>
<meta name="description" content="Meta description coerente e completa sobre o tema do artigo.">
<link rel="canonical" href="https://praia.digital/blog/conteudo-genérico.html">
</head>
<body>
<h1>Conteúdo genérico</h1>
<h2>Seção Um</h2><p>{"Conteúdo genérico sem informação específica. " * 20}</p>
<h2>Seção Dois</h2><p>{"Mais conteúdo genérico preenchendo estrutura. " * 20}</p>
<a href="/blog/artigo-completo.html">Leia mais</a>
</body>
</html>"""
    results.append(run_case('F1', 'Metadata completa + conteúdo genérico', f1_html, True))

    # G1: Repetição distribuída em 3 seções
    g1_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Repetição distribuída</title>
<meta name="description" content="Repetição distribuída: teste de detecção.">
<link rel="canonical" href="https://praia.digital/blog/repeticao-distribuida.html">
</head>
<body>
<h1>Repetição distribuída</h1>
<h2>Parte Um</h2><p>{"Aluguel de temporada exige gestão profissional. " * 10}</p>
<h2>Parte Dois</h2><p>{"Imóvel no litoral exige avaliação cuidadosa. " * 10}</p>
<h2>Parte Três</h2><p>{"Dica reduz risco quando bem aplicada. " * 10}</p>
<a href="/blog/artigo-completo.html">Leia mais</a>
</body>
</html>"""
    results.append(run_case('G1', 'Repetição distribuída em 3 seções', g1_html, True))

    # K1: Genérico longo + 2H2 + metadata + link
    k1_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Combinação K1</title>
<meta name="description" content="Meta description coerente e válida.">
<link rel="canonical" href="https://praia.digital/blog/combinacao-k1.html">
</head>
<body>
<h1>Combinação K1</h1>
<h2>Gestão</h2><p>{"Aluguel de temporada exige gestão profissional. " * 30}</p>
<h2>Avaliação</h2><p>{"Imóvel no litoral exige avaliação cuidadosa. " * 30}</p>
<a href="/blog/artigo-completo.html">Leia mais</a>
</body>
</html>"""
    results.append(run_case('K1', 'Genérico longo + 2H2 + metadata + link', k1_html, True))

    # K2: Lorem longo + 2H2 + metadata + link
    k2_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Combinação K2</title>
<meta name="description" content="Meta description válida e coerente com o artigo.">
<link rel="canonical" href="https://praia.digital/blog/combinacao-k2.html">
</head>
<body>
<h1>Combinação K2</h1>
<h2>Seção A</h2><p>{"Lorem ipsum dolor sit amet. " * 30}</p>
<h2>Seção B</h2><p>{"Consectetur adipiscing elit. " * 30}</p>
<a href="/blog/artigo-completo.html">Leia mais</a>
</body>
</html>"""
    results.append(run_case('K2', 'Lorem longo + 2H2 + metadata + link', k2_html, True))

    # K3: Palavras repetidas + 2H2 + metadata + link
    k3_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Combinação K3</title>
<meta name="description" content="Meta description válida e coerente.">
<link rel="canonical" href="https://praia.digital/blog/combinacao-k3.html">
</head>
<body>
<h1>Combinação K3</h1>
<h2>Tópico</h2><p>{"Palavra " * 200}</p>
<h2>Outro</h2><p>{"Palavra " * 200}</p>
<a href="/blog/artigo-completo.html">Leia mais</a>
</body>
</html>"""
    results.append(run_case('K3', 'Palavras repetidas + 2H2 + metadata + link', k3_html, True))

    # K5: 3 padrões genéricos diferentes + 3H2
    k5_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Combinação K5</title>
<meta name="description" content="Meta description válida.">
<link rel="canonical" href="https://praia.digital/blog/combinacao-k5.html">
</head>
<body>
<h1>Combinação K5</h1>
<h2>A</h2><p>{"Aluguel de temporada exige gestão profissional de reservas. " * 25}</p>
<h2>B</h2><p>{"Imóvel no litoral investimento imóvel usado exige avaliação. " * 25}</p>
<h2>C</h2><p>{"Investimento exige inspeção antes da decisão. " * 25}</p>
<a href="/blog/artigo-completo.html">Leia mais</a>
</body>
</html>"""
    results.append(run_case('K5', '3 padrões genéricos diferentes + 3H2', k5_html, True))

    # Verificar resultados
    print("=== REVALIDAÇÃO DOS 7 FALSOS NEGATIVOS DA E.1.8.1 ===")
    print()
    
    all_blocked = True
    for r in results:
        status = 'BLOCK' if r['blocked'] else 'PASS'
        expected = 'BLOCK' if r['expected_block'] else 'PASS'
        match = 'OK' if r['blocked'] == r['expected_block'] else 'FALHA'
        
        print(f"{r['case_id']}: {status} (esperado: {expected}) [{match}]")
        print(f"  Descrição: {r['description']}")
        print(f"  Palavras: {r['words']}, Bytes: {r['size']}, H2s: {r['h2_count']}, Links: {r['internal_links']}")
        
        if r['blocked'] and r['issues']:
            print(f"  Regras violadas:")
            for issue in r['issues']:
                print(f"    - {issue['rule']}: {issue['reason']}")
        print()
        
        if not r['blocked']:
            all_blocked = False
    
    print("=== RESUMO ===")
    blocked = sum(1 for r in results if r['blocked'])
    print(f"Total: {len(results)}")
    print(f"BLOCK: {blocked}/{len(results)}")
    print(f"PASS: {len(results) - blocked}/{len(results)}")
    
    if all_blocked:
        print()
        print("✓ TODOS OS 7 FALSOS NEGATIVOS FORAM BLOQUEADOS COM SUCESSO")
    else:
        print()
        print("✗ ALGUNS FALSOS NEGATIVOS PERMANECEM PASSANDO")


if __name__ == '__main__':
    main()
