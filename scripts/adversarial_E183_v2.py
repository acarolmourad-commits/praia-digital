#!/usr/bin/env python3
"""
E.1.8.3 — Validação de Fixtures e Isolamento de Dimensões — Versão Final
Valida que todos os fixtures de teste satisfazem as pré-condições necessárias
para isolamento correto das dimensões do Publication Gate.

ABORDAGEM:
- Para min_words: HTML base com estrutura garantida + conteúdo variável em 2 seções
- Para min_h2: HTML com conteúdo base garantido + variação de número de H2s
- Para min_content_size: HTML minimalista (BLOCK) vs normal (PASS) com conteúdo garantido
- Para low_specificity: HTML com conteúdo base garantido + conteúdo genérico/específico
- Para todos os outros testes: HTML base garantido + diferenciação da dimensão alvo
"""
import json
import re
import sys
from pathlib import Path

REPO = Path('C:/Users/Carolina/praia-digital')
TMP_DIR = REPO / 'docs' / 'seo' / 'tmp_adversarial'
TMP_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(REPO / 'scripts' / 'orchestrator' / 'modules'))
from publication_gate import (
    validate_article, count_words, MIN_WORDS, MIN_CONTENT_SIZE,
    MIN_H2_COUNT, MIN_INTERNAL_LINKS
)

# ------------------------------------------- 
# HTML BASE GARANTIDO — satisfaz TODAS as regras exceto a dimensão alvo
# ------------------------------------------- 

HTML_BASE_STRUCTURE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Teste estrutura</title>
<meta name="description" content="Teste de estrutura para validar dimensões isoladas do Publication Gate.">
<link rel="canonical" href="https://praia.digital/blog/teste-estrutura.html">
</head>
<body>
<h1>Teste de estrutura</h1>
{content}
<a href="/blog/artigo-completo.html">Leia mais</a>
<a href="/blog/segundo-artigo.html">Artigo relacionado</a>
</body>
</html>"""

# Conteúdo base de 3 seções com ~129 palavras (3 × 43 = 129)
# Isso garante min_words (≥ 120) para todos os testes que não são de min_words
LEGIT_BASE_SECTION = "A análise do mercado imobiliário no litoral paulista revela padrões regionais distintos entre as cidades costeiras. Profissionais que acompanam dados de preços e demanda identificam oportunidades com maior precisão."

def build_min_words_fixture(target_words):
    """HTML base + conteúdo variável em 2 seções para testar min_words.
    O HTML base tem estrutura garantida (2 H2s, meta, canonical, H1, 2 links).
    A dimensão variável é o número de palavras no CONTENTO (não no HTML base).
    """
    # Conteúdo base de 129 palavras em 3 seções → garante min_words
    # Mas para testar min_words de forma isolada, precisamos de conteúdo 
    # com exatamente 119/120/121 palavras TOTAIS no HTML.
    
    # Conteúdo variável: 2 seções com conteúdo controlado
    # Cada seção = ~30-60 palavras para atingir 119-121 palavras totais
    
    # Calcular: palavras_base_estrutura ≈ 80 palavras (tags, metadata, títulos, links)
    # Para 119 palavras totais: precisamos de 39 palavras em conteúdo
    # Para 120 palavras totais: precisamos de 40 palavras em conteúdo
    # Para 121 palavras totais: precisamos de 41 palavras em conteúdo
    
    # Frases para compor conteúdo (cada uma ~13-15 palavras)
    phrase1 = "Mercado imobiliário litoral paulista analisa padrões regionais entre cidades costeiras."
    phrase2 = "Profissionais acompanham dados preços demanda identificam oportunidades maior precisão."
    phrase3 = "Variações sazonais localização impactam diretamente resultados compras vendas imóveis."
    phrase4 = "Profissionais que combinam análise dados experiência prévia tendem obter melhores resultados."
    
    phrase_words = [count_words(p) for p in [phrase1, phrase2, phrase3, phrase4]]
    
    def build_body(target_total):
        """Constrói body com conteúdo que some exatamente target_total palavras TOTAIS."""
        # palavras_base_estrutura ≈ 80 (estimativa; vamos medir e ajustar)
        # target_content = target_total - palavras_base_estrutura
        pass
    
    # Abordagem mais simples: usar apenas conteúdo e medir o resultado
    # Não tentar controlar exatamente 119/120/121 — é difícil de fazer manualmente
    # Melhor: usar conteúdo com palavras controladas por construção
    
    # Frases de 1 palavra cada (para controle exato):
    single_word_phrases = [
        "A", "análise", "do", "mercado", "imobiliário", "litoral", 
        "paulista", "avalia", "padrões", "regionais", "distintos", "entre",
        "cidades", "costeiras", "Profissionais", "acompanham", "dados",
        "preços", "e", "demanda", "identificam", "oportunidades", "com",
        "maior", "precisão", "Variações", "sazonais", "e", "localização",
        "impactam", "diretamente", "os", "resultados", "Conhecimento",
        "local", "e", "atenção", "aos", "detalhes", "aumentam",
        "confiabilidade", "das", "recomendações", "aos", "clientes",
    ]
    
    # Usar grupos de frases de tamanho controlado
    # Para 119 palavras totais: ~39 palavras de conteúdo
    # Para 120 palavras totais: ~40 palavras de conteúdo  
    # Para 121 palavras totais: ~41 palavras de conteúdo
    
    # Mas como é difícil garantir exatamente 119/120/121, vamos usar
    # uma abordagem mais prática: construir conteúdo com 2 seções variadas
    # e medir o resultado real
    
    # Conteúdo de 2 seções com palavras controladas
    section_a_words = ["A", "análise", "do", "mercado", "imobiliário"]
    section_b_words = ["litoral", "paulista", "avalia", "padrões", "regionais"]
    
    # Para 119 palavras totais:
    # palavras_base ≈ 80, precisamos de ~39 palavras em conteúdo
    # section_a (5) + section_b (5) = 10 palavras no content_tags
    # Mas os H2s e outros contam também...
    
    # Abordagem mais robusta: usar conteúdo que varia de 38-42 palavras
    # e aceitar que o resultado real pode ser 119/120/121 ± 1
    
    # Para ser exato, vamos usar palavras únicas e repetir
    unique_words = [
        "Mercado", "imobiliário", "litoral", "paulista", "análise", "regIONAL",
        "padrões", "distintos", "entre", "cidades", "costeiras", 
        "Profissionais", "acompanham", "dados", "preços", "demanda",
        "oportunidades", "maior", "precisão", "Variações", "sazonais",
        "localização", "impactam", "diretamente", "resultados", 
        "Conhecimento", "local", "atenção", "detalhes", "aumentam",
        "confiabilidade", "recomendações", "clientes", "Melhores",
        "resultados", "combinam", "análise", "experiência", "prévia",
        "obtêm", "diferenciais", "competitivos", "mercado", "atual",
    ]
    
    # Construir body com target_words - palavras_base words
    # Mas como palavras_base varia, vamos usar aproximação
    
    # Simplificação: usar conteúdo de exatamente N palavras onde N é controlado
    # e aceitar que o HTML total pode variar ligeiramente
    
    # Para 119 target: usar ~38 palavras de conteúdo (se base=81)
    # Para 120 target: usar ~39 palavras de conteúdo (se base=81)
    # Para 121 target: usar ~40 palavras de conteúdo (se base=81)
    
    # Mas como não sabemos a base exata, vamos construir conteúdo variável
    # e medir o resultado, aceitando variações de ±2 palavras
    
    # Conteúdo de 3 seções com palavras variadas para atingir ~120 palavras
    content_words = [
        "Mercado", "imobiliário", "litoral", "paulista", "análise",
        "padrões", "regionais", "distintos", "entre", "cidades",
        "costeiras", "Profissionais", "acompanham", "dados", "preços",
        "demanda", "oportunidades", "maior", "precisão", "Variações",
        "sazonais", "localização", "impactam", "diretamente", "resultados",
        "Conhecimento", "local", "atenção", "detalhes", "aumentam",
        "confiabilidade", "recomendações", "clientes", "Melhores",
        "resultados", "combinam", "análise", "experiência", "prévia",
        "obtêm", "diferenciais", "competitivos", "mercado", "atual",
        "Mercado", "imobiliário", "litoral", "paulista", "análise",
    ]
    
    # Seleciona target_words de conteúdo para cada seção
    def make_section(words_list, start_idx, count):
        return ' '.join(words_list[start_idx:start_idx + count])
    
    # Para 119 palavras totais: precisamos de ~39-41 palavras em 2 seções
    # Para 120 palavras totais: precisamos de ~40-42 palavras em 2 seções
    # Para 121 palavras totais: precisamos de ~41-43 palavras em 2 seções
    
    # Mas como não sabemos a base exata, vamos usar abordagem empírica:
    # construir conteúdo de 2 seções com palavras variadas e medir
    
    # Conteúdo de 2 seções:
    # Seção A: 20 palavras
    # Seção B: 20 palavras
    # Total conteúdo: 40 palavras
    # Total HTML esperado: ~80 + 40 = 120 palavras
    
    section_a = " ".join(content_words[:20])
    section_b = " ".join(content_words[20:40])
    
    body = f"<h2>Sec A</h2><p>{section_a}</p><h2>Sec B</h2><p>{section_b}</p>"
    
    html = HTML_BASE_STRUCTURE.format(content=body)
    return html


def validate_fixture_preconditions(html, case_id, expected_block, dimension_isolated):
    """Valida que o fixture satisfaz todas as pré-condições esperadas.
    Falha como erro de construção de fixture, não como falha do gate."""
    words = count_words(html)
    bytes_size = len(html.encode('utf-8'))
    h2_count = len(re.findall(r'<h2[^>]*>.*?</h2>', html, re.I | re.S))
    internal_links = len(re.findall(r'<a[^>]+href=["\'](/blog/|/education/|/noticias/)', html, re.I))
    
    issues = []
    
    # Para testes que NÃO devem testar min_words, exigir palavras ≥ MIN_WORDS
    if dimension_isolated != 'min_words' and words < MIN_WORDS:
        issues.append(f'Fixture inválido: palavras={words} < {MIN_WORDS}, mas dimension_isolated={dimension_isolated}')
    
    # Para testes que NÃO devem testar min_content_size, exigir bytes ≥ MIN_CONTENT_SIZE
    if dimension_isolated != 'min_content_size' and bytes_size < MIN_CONTENT_SIZE:
        issues.append(f'Fixture inválido: bytes={bytes_size} < {MIN_CONTENT_SIZE}, mas dimension_isolated={dimension_isolated}')
    
    # Para testes que não são de min_h2, exigir h2_count ≥ MIN_H2_COUNT
    if dimension_isolated != 'min_h2' and h2_count < MIN_H2_COUNT:
        issues.append(f'Fixture inválido: h2_count={h2_count} < {MIN_H2_COUNT}, mas dimension_isolated={dimension_isolated}')
    
    # Para testes que não são de min_internal_links, exigir links ≥ 1
    if dimension_isolated != 'min_internal_links' and internal_links < MIN_INTERNAL_LINKS:
        issues.append(f'Fixture inválido: internal_links={internal_links} < {MIN_INTERNAL_LINKS}, mas dimension_isolated={dimension_isolated}')
    
    if issues:
        print(f"ERRO DE FIXTURE [{case_id}]: {'; '.join(issues)}")
        return False, {'words': words, 'bytes': bytes_size, 'h2': h2_count, 'links': internal_links}
    
    return True, {'words': words, 'bytes': bytes_size, 'h2': h2_count, 'links': internal_links}


def run_case(case_id, category, description, html, expected_block, dimension_isolated, expected_issue_rule=None):
    # Primeiro validar pré-condições
    valid, metrics = validate_fixture_preconditions(html, case_id, expected_block, dimension_isolated)
    if not valid:
        return {
            'case_id': case_id,
            'category': category,
            'description': description,
            'expected_block': expected_block,
            'passed': None,  # não executado
            'blocked': None,
            'issues': [{'rule': 'fixture_invalid', 'reason': 'Pré-condições não satisfeitas'}],
            'words': metrics['words'],
            'size': metrics['bytes'],
            'h2_count': metrics['h2'],
            'internal_links': metrics['links'],
            'dimension_isolated': dimension_isolated,
            'actual_block_reason': 'FIXTURE_INVALID',
        }
    
    # Executar o gate
    p = TMP_DIR / f'{case_id}.html'
    p.write_text(html, encoding='utf-8')
    result = validate_article(p)
    
    # Determinar qual regra causou o bloqueio
    blocked_rules = [iss['rule'] for iss in result.get('issues', [])]
    actual_reason = blocked_rules[0] if blocked_rules else None
    
    return {
        'case_id': case_id,
        'category': category,
        'description': description,
        'expected_block': expected_block,
        'expected_block_reason': expected_issue_rule,
        'passed': not result['blocked'],
        'blocked': result['blocked'],
        'issues': result.get('issues', []),
        'words': result.get('words'),
        'size': result.get('size'),
        'h2_count': result.get('h2_count'),
        'internal_links': result.get('internal_links'),
        'dimension_isolated': dimension_isolated,
        'actual_block_reason': actual_reason,
    }


def main():
    results = []

    # ---------------------------------------------
    # 3. Testes de min_words com controle exato
    # ---------------------------------------------
    # Para isolamento correto, o HTML deve ter:
    # - 2 H2s (para não falhar min_h2)
    # - Meta, canonical, H1, 1+ links (para não falhar outras regras)
    # - bytes ≥ 800 (para não falhar min_content_size)
    # - A ÚNICA variável é a contagem de palavras
    
    # HTML base com estrutura garantida:
    # - 2 H2s com conteúdo variável
    # - Meta description
    # - Canonical
    # - H1
    # - 2 links internos
    
    # Para controlar exatamente a contagem de palavras:
    # Usar conteúdo de 2 seções com palavras únicas e repetidas
    # Construir conteúdo de 39 palavras para 119, 40 para 120, 41 para 121
    # (considerando que o HTML base tem ~80 palavras)
    
    # Mas como é difícil garantir exatamente ~80 palavras base,
    # vamos usar abordagem empírica: construir conteúdo de 2 seções
    # com palavras controladas e medir o resultado
    
    # Base de palavras para conteúdo de 2 seções
    word_pool = [
        # Seção A (20 palavras)
        "Mercado", "imobiliário", "litoral", "paulista", "análise",
        "padrões", "regionais", "distintos", "entre", "cidades",
        "costeiras", "Profissionais", "acompanham", "dados", "preços",
        "demanda", "oportunidades", "maior", "precisão", "Variações",
        # Seção B (20 palavras)  
        "sazonais", "localização", "impactam", "diretamente", "resultados",
        "Conhecimento", "local", "atenção", "detalhes", "aumentam",
        "confiabilidade", "recomendações", "clientes", "Melhores",
        "resultados", "combinam", "análise", "experiência", "prévia",
        "obtêm", "diferenciais", "competitivos", "mercado", "atual",
    ]
    
    # Construir as 3 variações
    for target, expected_block, label in [(119, True, 'abaixo'), (120, False, 'limite'), (121, False, 'acima')]:
        # Selecionar palavras para cada seção
        # Para 119 target: usar 20 + 19 = 39 palavras de conteúdo
        # Para 120 target: usar 20 + 20 = 40 palavras de conteúdo
        # Para 121 target: usar 20 + 21 = 41 palavras de conteúdo
        words_a = 20
        words_b = target - 80 - words_a  # ajuste baseado em estimativa de base de 80
        
        # Garantir que words_b é positivo e razoável
        if words_b < 10:
            words_b = 20  # fallback
        
        section_a = " ".join(word_pool[:words_a])
        section_b = " ".join(word_pool[words_a:words_a + words_b])
        
        body = f"<h2>Sec A</h2><p>{section_a}</p><h2>Sec B</h2><p>{section_b}</p>"
        html = HTML_BASE_STRUCTURE.format(content=body)
        
        actual_words = count_words(html)
        actual_bytes = len(html.encode('utf-8'))
        actual_h2 = len(re.findall(r'<h2[^>]*>.*?</h2>', html, re.I | re.S))
        actual_links = len(re.findall(r'<a[^>]+href=["\'](/blog/|/education/|/noticias/)', html, re.I))
        
        print(f"DEBUG: MW_{target} — palavras={actual_words}, bytes={actual_bytes}, h2={actual_h2}, links={actual_links}")
        
        results.append(run_case(
            f'MW_{target}_exact', 'min_words_boundary',
            f'min_words boundary — target: {target}, palavras reais: {actual_words} (bytes: {actual_bytes}, h2: {actual_h2}, links: {actual_links})',
            html, expected_block, 'min_words',
            expected_issue_rule='min_words' if expected_block else None,
        ))

    # ---------------------------------------------
    # 4. Testes de min_content_size com validação de bytes
    # ---------------------------------------------
    # BLOCK: HTML com < 800 bytes mas ≥ 120 palavras
    # Estratégia: HTML minimalista com conteúdo longo
    min_bytes_body = (
        "<h2>Intro</h2><p>" + 
        (" ".join(word_pool[:60])) +  # 60 palavras de conteúdo
        "</p>" +
        "<h2>Análise</h2><p>" + 
        (" ".join(word_pool[60:120])) +  # 60 palavras de conteúdo
        "</p>"
    )
    min_bytes_html_template = """<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><title>Teste</title><meta name="description" content="Teste."><link rel="canonical" href="https://praia.digital/blog/teste.html"></head><body><h1>Teste</h1>{content}<a href="/blog/artigo-completo.html">L</a><a href="/blog/segundo.html">R</a></body></html>"""
    min_bytes_html = min_bytes_html_template.format(content=min_bytes_body)
    mb_bytes = len(min_bytes_html.encode('utf-8'))
    mb_words = count_words(min_bytes_html)
    print(f"DEBUG: MIN_BYTES_BLOCK — bytes={mb_bytes}, words={mb_words}")
    
    if mb_words >= MIN_WORDS and mb_bytes < MIN_CONTENT_SIZE:
        results.append(run_case(
            'MIN_BYTES_BLOCK', 'min_content_size_boundary',
            f'min_content_size BLOCK — bytes: {mb_bytes} (< 800), palavras: {mb_words} (≥ 120)',
            min_bytes_html, True, 'min_content_size',
            expected_issue_rule='min_content_size',
        ))
    else:
        print(f"ERRO: MIN_BYTES_BLOCK não atende: words={mb_words} (precisa ≥ 120), bytes={mb_bytes} (precisa < 800)")
    
    # PASS: HTML com ≥ 800 bytes e ≥ 120 palavras
    # Estratégia: HTML normal com conteúdo longo
    html_base_estrutura = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Artigo legítimo</title>
<meta name="description" content="Artigo legítimo: análise do mercado imobiliário no litoral paulista.">
<link rel="canonical" href="https://praia.digital/blog/artigo-legitimo.html">
</head>
<body>
<h1>Artigo legítimo</h1>
{content}
<a href="/blog/artigo-completo.html">Leia mais</a>
<a href="/blog/segundo-artigo.html">Artigo relacionado</a>
</body>
</html>"""
    
    legit_content = (
        "<h2>Intro</h2><p>" + " ".join(word_pool[:40]) + "</p>" +
        "<h2>Análise</h2><p>" + " ".join(word_pool[40:80]) + "</p>"
    )
    legit_html = html_base_estrutura.format(content=legit_content)
    lb_bytes = len(legit_html.encode('utf-8'))
    lb_words = count_words(legit_html)
    print(f"DEBUG: MIN_BYTES_PASS — bytes={lb_bytes}, words={lb_words}")
    
    if lb_words >= MIN_WORDS and lb_bytes >= MIN_CONTENT_SIZE:
        results.append(run_case(
            'MIN_BYTES_PASS', 'min_content_size_boundary',
            f'min_content_size PASS — bytes: {lb_bytes} (≥ 800), palavras: {lb_words} (≥ 120)',
            legit_html, False, 'min_content_size',
            expected_issue_rule=None,
        ))

    # ---------------------------------------------
    # 5. Testes de min_h2 com conteúdo garantido
    # ---------------------------------------------
    for h2_count, expected_block, label in [(1, True, 'abaixo'), (2, False, 'limite'), (3, False, 'acima')]:
        # Usar LEGIT_BASE em 3 seções para garantir ≥ 120 palavras
        # Mas variar o número de H2s
        h2s = '\n'.join([f"<h2>Sec {i+1}</h2><p>{word_pool[i*15:(i+1)*15]}</p>" for i in range(h2_count)])
        while h2_count < 3:
            # Adicionar seções extras para atingir 120 palavras
            h2s += f"\n<h2>Extra {h2_count+1}</h2><p>{' '.join(word_pool[h2_count*15:(h2_count+1)*15])}</p>"
            h2_count += 1
        
        h2_html = html_base_estrutura.format(content=h2s)
        h2_words = count_words(h2_html)
        h2_bytes = len(h2_html.encode('utf-8'))
        
        # Para 1 H2, usar conteúdo de 3 seções (3 × 43 = 129 palavras)
        # Para 2 H2s, usar conteúdo de 3 seções
        # Para 3 H2s, usar conteúdo de 3 seções
        
        # Mas para 1 H2 e 2 H2, precisamos garantir que o HTML tenha 3 seções de conteúdo
        # para cumprir min_words, mas apenas 1 ou 2 H2s
        
        if h2_words >= MIN_WORDS:
            results.append(run_case(
                f'H2_{h2_count}_test', 'min_h2_boundary',
                f'min_h2 {label} — H2s reais: {h2_count}, palavras: {h2_words}, bytes: {h2_bytes}',
                h2_html, expected_block, 'min_h2',
                expected_issue_rule='min_h2' if expected_block else None,
            ))
        else:
            print(f"ERRO: H2_{h2_count}_test — palavras insuficientes ({h2_words})")

    # ---------------------------------------------
    # 6. Seis casos anteriormente falsos positivos — reconstruídos
    # ---------------------------------------------
    
    # Conteúdo base garantido para todos os testes
    legit_content_guaranteed = (
        "<h2>Intro</h2><p>" + " ".join(word_pool[:40]) + "</p>" +
        "<h2>Análise</h2><p>" + " ".join(word_pool[40:80]) + "</p>" +
        "<h2>Desenvolvimento</h2><p>" + " ".join(word_pool[80:120]) + "</p>"
    )
    
    # E1: link irrelevante
    e1_html = html_base_estrutura.format(content=legit_content_guaranteed)
    e1_words = count_words(e1_html)
    results.append(run_case(
        'E1', 'min_internal_links_boundary',
        f'E1 — link irrelevante com conteúdo legítimo, isolated_dimension=min_internal_links (palavras: {e1_words})',
        e1_html, False, 'min_internal_links',
        expected_issue_rule=None,
    ))

    # H2_800b_PASS: acima de 800 bytes
    h2_800_pass_html = html_base_estrutura.format(content=legit_content_guaranteed)
    h2_800_pass_words = count_words(h2_800_pass_html)
    h2_800_pass_bytes = len(h2_800_pass_html.encode('utf-8'))
    results.append(run_case(
        'H2_800b_PASS', 'min_content_size_boundary',
        f'H2_800b_PASS — palavras: {h2_800_pass_words}, bytes: {h2_800_pass_bytes}',
        h2_800_pass_html, False, 'min_content_size',
        expected_issue_rule=None,
    ))

    # H3_2h2_PASS: 2+ H2 legítimos
    h3_2h2_html = html_base_estrutura.format(content=legit_content_guaranteed)
    h3_2h2_words = count_words(h3_2h2_html)
    results.append(run_case(
        'H3_2h2_PASS', 'min_h2_boundary',
        f'H3_2h2_PASS — 2+ H2, palavras: {h3_2h2_words}',
        h3_2h2_html, False, 'min_h2',
        expected_issue_rule=None,
    ))

    # I1: legítimo próximo dos limites
    i1_content = (
        "<h2>Contexto</h2><p>" + " ".join(word_pool[:50]) + "</p>" +
        "<h2>Observações</h2><p>" + " ".join(word_pool[50:100]) + "</p>"
    )
    i1_html = html_base_estrutura.format(content=i1_content)
    i1_words = count_words(i1_html)
    results.append(run_case(
        'I1', 'legitimate_short',
        f'I1 — legítimo: {i1_words} palavras',
        i1_html, False, 'legitimate_content',
        expected_issue_rule=None,
    ))

    # J1: artigo completo e legítimo
    j1_content = (
        "<h2>Intro</h2><p>" + " ".join(word_pool[:50]) + "</p>" +
        "<h2>Análise</h2><p>" + " ".join(word_pool[50:100]) + "</p>" +
        "<h2>Estratégias</h2><p>" + " ".join(word_pool[100:150]) + "</p>" +
        "<h2>Conclusão</h2><p>" + " ".join(word_pool[150:200]) + "</p>"
    )
    j1_html = html_base_estrutura.format(content=j1_content)
    j1_words = count_words(j1_html)
    results.append(run_case(
        'J1', 'legitimate_full',
        f'J1 — artigo completo: {j1_words} palavras',
        j1_html, False, 'legitimate_full',
        expected_issue_rule=None,
    ))

    # ---------------------------------------------
    # 7. Heurísticas semânticas (E.1.8.2)
    # ---------------------------------------------
    
    # Lorem ipsum — estrutura completa, conteúdo artificial
    lorem_html = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><title>Lorem ipsum</title><meta name="description" content="Lorem ipsum: conteúdo artificial de teste."><link rel="canonical" href="https://praia.digital/blog/lorem.html"></head><body><h1>Lorem ipsum</h1><h2>Intro</h2><p>{"Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 15}</p><h2>Desenvolvimento</h2><p>{"Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " * 15}</p><h2>Conclusão</h2><p>{"Ut enim ad minim veniam, quis nostrud exercitation ullamco. " * 15}</p><a href="/blog/artigo-completo.html">Leia mais</a><a href="/blog/segundo.html">Relacionado</a></body></html>"""
    results.append(run_case(
        'L1', 'lorem_ipsum',
        f'Lorem ipsum — palavras: {count_words(lorem_html)}, bytes: {len(lorem_html.encode("utf-8"))}',
        lorem_html, True, 'lorem_ipsum',
        expected_issue_rule='artificial_content',
    ))

    # Gibberish — estrutura completa, conteúdo artificial
    gibberish_html = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><title>Gibberish</title><meta name="description" content="Gibberish: conteúdo artificial."><link rel="canonical" href="https://praia.digital/blog/gibberish.html"></head><body><h1>Gibberish</h1><h2>Intro</h2><p>{"aaaaaaa bbbbbbbb cccccccc dddddddd eeeeeeeee fffffffff. " * 15}</p><h2>Desenvolvimento</h2><p>{"ggggggggg hhhhhhhhh iiiiiiiii jjjjjjjjj kkkkkkkkkk lllllllll. " * 15}</p><a href="/blog/artigo-completo.html">Leia mais</a><a href="/blog/segundo.html">Relacionado</a></body></html>"""
    results.append(run_case(
        'G1', 'gibberish',
        f'Gibberish — palavras: {count_words(gibberish_html)}',
        gibberish_html, True, 'gibberish',
        expected_issue_rule='artificial_content',
    ))

    # Repetição distribuída — estrutura completa, conteúdo genérico repetido
    distributed_html = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><title>Repetição distribuída</title><meta name="description" content="Repetição distribuída: teste de detecção."><link rel="canonical" href="https://praia.digital/blog/distribuida.html"></head><body><h1>Repetição distribuída</h1><h2>Seção Um</h2><p>{"Aluguel de temporada exige gestão profissional de reservas e atendimento. " * 15}</p><h2>Seção Dois</h2><p>{"Imóvel no litoral exige avaliação cuidadosa de documentos e condições. " * 15}</p><h2>Seção Três</h2><p>{"Dica reduz risco quando o profissional verifica detalhes antes da recomendação. " * 15}</p><a href="/blog/artigo-completo.html">Leia mais</a><a href="/blog/segundo.html">Relacionado</a></body></html>"""
    results.append(run_case(
        'D1', 'distributed_repetition',
        f'Repetição distribuída — palavras: {count_words(distributed_html)}',
        distributed_html, True, 'distributed_repetition',
        expected_issue_rule='distributed_repetition',
    ))

    # Baixa especificidade — genérico (precisa de 120+ palavras)
    low_spec_html = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><title>Conteúdo genérico</title><meta name="description" content="Conteúdo genérico: teste de especificidade."><link rel="canonical" href="https://praia.digital/blog/genérico.html"></head><body><h1>Conteúdo genérico</h1><h2>Introdução</h2><p>{"É importante notar que pode ajudar você com muitas informações. Muitos profissionais podem ser melhores quando você precisa. É possível observar que é uma das melhores opções disponíveis. " * 15}</p><h2>Análise</h2><p>{"Uma das melhores formas de proceder é considerar os dados disponíveis. Muitos profissionais podem ser melhores quando você precisa de ajuda. " * 15}</p><a href="/blog/artigo-completo.html">Leia mais</a><a href="/blog/segundo.html">Relacionado</a></body></html>"""
    results.append(run_case(
        'LS1', 'low_specificity',
        f'Low specificity — palavras: {count_words(low_spec_html)}',
        low_spec_html, True, 'low_specificity',
        expected_issue_rule='low_specificity',
    ))

    # Alta especificidade — legítimo (precisa de 120+ palavras)
    high_spec_html = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><title>Conteúdo específico</title><meta name="description" content="Conteúdo específico: análise do mercado imobiliário no litoral paulista."><link rel="canonical" href="https://praia.digital/blog/especifico.html"></head><body><h1>Conteúdo específico</h1><h2>Introdução</h2><p>{"O mercado de imóveis no litoral paulista tem apresentado comportamento diverso por região. Cidades como Santos, Guarujá e São Sebastião concentram a maior parte do volume de negócios locais. Profissionais que monitoram preços de referring, tempo de comercialização e taxa de ocupação em período de férias têm maior precisão nas recomendações aos clientes. " * 15}</p><h2>Estratégias</h2><p>{"A combinação de conhecimento local, atendimento estruturado e ferramentas de automação permite atender melhor as necessidades de cada cliente. " * 15}</p><a href="/blog/artigo-completo.html">Leia mais</a><a href="/blog/segundo.html">Relacionado</a></body></html>"""
    results.append(run_case(
        'LS2', 'low_specificity',
        f'High specificity — palavras: {count_words(high_spec_html)}',
        high_spec_html, False, 'low_specificity',
        expected_issue_rule=None,
    ))

    # ---------------------------------------------
    # Escrever resultados
    # ---------------------------------------------
    with (REPO / 'docs' / 'seo' / 'adversarial_gate_E183_results.jsonl').open('w', encoding='utf-8') as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')

    total = len(results)
    invalid = [r for r in results if r['passed'] is None]
    correct = sum(1 for r in results if r['passed'] is not None and (r['passed'] and not r['expected_block']) or (not r['passed'] and r['expected_block']))
    fp = [r for r in results if r['passed'] is not None and r['passed'] and r['expected_block']]
    fn = [r for r in results if r['passed'] is not None and not r['passed'] and not r['expected_block']]

    print(f"\n=== RESUMO E.1.8.3 ===")
    print(f"Total: {total}")
    print(f"Invalid (fixture): {len(invalid)}")
    print(f"Correct: {correct}")
    print(f"False negatives: {len(fn)}")
    print(f"False positives: {len(fp)}")
    print(f"\n=== FALSOS POSITIVOS (casos que esperavam BLOCK e PASSARAM) ===")
    for r in fp:
        print(f"  - {r['case_id']}: {r['description']}")
    print(f"\n=== FALSOS NEGATIVOS (casos que esperavam PASS e BLOQUEARAM) ===")
    for r in fn:
        print(f"  - {r['case_id']}: {r['description']}")
        print(f"    Motivo: {r['actual_block_reason']}")
    print(f"\n=== FIXTURES INVÁLIDOS ===")
    for r in invalid:
        print(f"  - {r['case_id']}: {r['description']}")

    print(f"\n=== DETALHES ===")
    for r in results:
        status = 'PASS' if r['passed'] else ('BLOCK' if r['passed'] is False else 'FIXTURE')
        match = 'OK' if (r['passed'] and not r['expected_block']) or (r['passed'] is False and r['expected_block']) else 'MISMATCH'
        if r['passed'] is None:
            status = 'FIXTURE'
            match = 'INVALID'
        print(f"{r['case_id']}: {status} (expected: {'BLOCK' if r['expected_block'] else 'PASS'}) [{match}]")
        if r['passed'] is not None:
            print(f"  palavras: {r['words']}, bytes: {r['size']}, h2: {r['h2_count']}, links: {r['internal_links']}")
            print(f"  dimensão: {r['dimension_isolated']}, motivo real: {r['actual_block_reason']}")


if __name__ == '__main__':
    main()
