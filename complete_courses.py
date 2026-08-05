import os

base = 'education/cursos'

cursos_incompletos = [
    'analise-de-rentabilidade',
    'automacao-comercial',
    'avaliacao-de-imoveis',
    'captacao-exclusividade',
    'casa-ou-apartamento',
    'comprar-com-seguranca',
    'comprar-imovel-praia-sem-golpes',
    'crm-para-corretores',
    'documentacao-imobiliaria',
    'especialista-venda-imoveis-litoral',
    'financiamento-imobiliario',
    'flipping',
    'funil-de-vendas',
    'guia-investidor-imobiliario',
    'ia-para-corretores',
    'ia-para-imobiliarias',
    'imoveis-para-airbnb',
    'instagram-para-corretores',
    'marketing-imobiliario',
    'multiplique-patrimonio',
    'primeiro-imovel-litoral',
    'ptam-na-pratica',
    'whatsapp-que-vende',
]

# arquivos que precisam existir em todos os cursos
required_dirs = [
    'curso-completo',
    'checklists',
    'planilhas',
    'avaliacao',
    'certificado',
    'ebook',
    'mini-curso',
    'email-sequence',
    'instagram',
    'seo-articles',
    'marketing',
]

required_files = [
    'index.html',
    'vendas.html',
    'curso-completo/ficha-completa.md',
    'curso-completo/sumario.md',
    'curso-completo/modulo-1.md',
    'curso-completo/modulo-2.md',
    'curso-completo/modulo-3.md',
    'curso-completo/modulo-4.md',
    'checklists/checklist-cadastro.md',
    'planilhas/planilha-precificacao.md',
    'avaliacao/avaliacao-final.md',
    'certificado/certificado.md',
    'ebook/lead-magnet.md',
    'mini-curso/sumario.md',
    'email-sequence/sequencia.md',
    'instagram/posts.md',
    'seo-articles/sumario.md',
    'marketing/webinar.md',
    'marketing/youtube.md',
    'marketing/meta-ads.md',
    'marketing/google-ads.md',
    'marketing/instagram-posts.md',
    'marketing/reels.md',
    'marketing/tiktok.md',
    'marketing/shorts.md',
    'marketing/faq.md',
]

# conteúdo placeholder mínimo
ficha_completa = """# Curso: {nome}
## Nome Comercial
**{nome}**

## Subtítulo
Curso completo sobre {nome} no litoral.

## Promessa Principal
Aprenda {nome} na prática.

## Público-alvo
- Proprietários e investidores
- Corretores e gestores

## Nível
Iniciante → Intermediário

## Tempo Estimado
4 horas

## Valor Sugerido
Curso completo: R$ 297

## Oferta Principal
- Acesso vitalício + atualizações
- Certificado

## Headline
**"Domine {nome} no litoral"**

## Big Idea
Conhecimento aplicado a {nome} gera resultado.

## Oferta
- **Curso completo:** R$ 297
- **E-book:** R$ 19,90

## Avatar
**Nome:** Maria / João
**Idade:** 25 a 50 anos
**Renda:** R$ 5k a R$ 25k/mês
**Objetivo:** aprender {nome}
**Dificuldades:** falta de método
**Desejos:** resultado rápido

## Dores
- Falta de método
- Falta de tempo
- Falta de suporte

## Desejos
- Método claro
- Resultado rápido
- Suporte

## Objeções
- "É complicado"
- "Não compensa"
- "Não tenho tempo"

## Transformação
- Método aplicado
- Resultados reais
- Segurança

## Programa Completo
### Módulo 1 — Fundamentos
Aula 1.1 — Introdução
Aula 1.2 — Conceitos essenciais
Aula 1.3 — Aplicação no litoral
Exercício: defina objetivo

### Módulo 2 — Método
Aula 2.1 — Passo 1
Aula 2.2 — Passo 2
Aula 2.3 — Passo 3
Exercício: aplique o método

### Módulo 3 — Execução
Aula 3.1 — Ações práticas
Aula 3.2 — Erros comuns
Aula 3.3 — Revisão
Exercício: plano de execução

### Módulo 4 — Resultado
Aula 4.1 — Indicadores
Aula 4.2 — Ajustes
Aula 4.3 — Escala
Exercício: monte o plano final

## Carga Horária
4 horas

## Material Complementar
- PDFs por módulo
- Comunidade fechada

## Checklists
- Checklist de preparação
- Checklist de execução

## Planilhas
- Planilha de acompanhamento

## Modelos Prontos
- Modelo de plano

## Scripts
- Script de apoio

## Prompt de IA
Prompt para criar plano de ação.

## Exercícios
- Exercício 1: objetivo
- Exercício 2: método
- Exercício 3: execução
- Exercício 4: revisão
- Exercício 5: plano final

## Avaliações
Quiz 20 perguntas
Prova prática: plano aplicado

## FAQ
1. Em quanto tempo vejo resultado? De 30 a 60 dias.
2. Preciso investir muito? Não.
3. Funciona para qualquer caso? Na maioria.
4. E se errar? Ajuste rápido.
5. Vale a pena? Sim.

## Página de Vendas
[vendas.html]

## Landing Page
[index.html]

## Sequência de E-mails
[email-sequence/sequencia.md]

## Posts Instagram
[instagram/posts.md]

## Reels
[marketing/reels.md]

## Carrosséis
[marketing/carrosseis.md]

## Artigos SEO
[seo-articles/sumario.md]

## Roteiros YouTube
[marketing/youtube.md]

## Anúncios Meta
[marketing/meta-ads.md]

## Anúncios Google
[marketing/google-ads.md]

## CTA
"Domine {nome} no litoral."

## Upsell
- Mentoria individual: R$ 1.500

## Downsell
- E-book: R$ 19,90

## Cross-sell
- Cursos complementares
"""

sumario = """# Sumário do Curso: {nome}
- Módulo 1: Fundamentos
- Módulo 2: Método
- Módulo 3: Execução
- Módulo 4: Resultado
"""

modulo = """# Módulo {modulo} — {titulo}
## Aula {modulo}.1 — Introdução
Conteúdo: conceitos e aplicação.

## Aula {modulo}.2 — Conceitos essenciais
Conteúdo: fundamentos e exemplos.

## Aula {modulo}.3 — Aplicação no litoral
Conteúdo: caso prático no litoral.

## Exercício
Aplique o conteúdo no seu contexto.
"""

checklist_cadastro = """# Checklist de {nome}
- [ ] Etapa 1
- [ ] Etapa 2
- [ ] Etapa 3
- [ ] Etapa 4
- [ ] Etapa 5
"""

planilha_precificacao = """# Planilha de {nome}
- [ ] Coluna 1
- [ ] Coluna 2
- [ ] Coluna 3
- [ ] Coluna 4
"""

avaliacao_final = """# Avaliação Final — {nome}
## Quiz
- 20 perguntas sobre o conteúdo do curso.

## Prova Prática
- Aplicação do método em um caso real.

## Critério de Aprovação
- 70% no quiz + prática aprovada pelo mentor.
"""

certificado = """# Certificado — {nome}
Modelo: Praia Digital Academy
Curso: {nome}
Carga horária: 4 horas
Aprovado: [nome]
Data: [data]
Código: [código único]
"""

ebook_lead_magnet = """# E-book Derivado — {nome}
Título: Guia Rápido de {nome} no Litoral
Formato: PDF 20 a 30 páginas
Preço: gratuito ou R$ 17,90
Conteúdo: checklist, templates, dicas rápidas.
"""

mini_curso_sumario = """# Mini Curso — {nome}
## Aula 1 — Introdução (8 min)
## Aula 2 — Conceitos essenciais (12 min)
## Aula 3 — Aplicação prática (10 min)
## Bônus — Template
"""

email_sequence = """# Sequência de E-mails — {nome}
## E-mail 1 — Entrega do lead magnet
Assunto: Guia Rápido de {nome} (PDF)
Conteúdo: acesso ao material + introdução ao curso completo
CTA: Quero o curso completo

## E-mail 2 — Case
Assunto: Case de {nome} no litoral
Conteúdo: passo a passo real
CTA: Ver curso completo

## E-mail 3 — Objeção
Assunto: “{nome} é complicado?”
Conteúdo: quebra de objeção com método
CTA: Começar agora

## E-mail 4 — Prova social
Assunto: Aluno aplicou o método
Conteúdo: depoimento + resultado
CTA: Participar do próximo lote

## E-mail 5 — Urgência
Assunto: Últimas vagas com bônus
Conteúdo: oferta limitada
CTA: Garantir minha vaga
"""

instagram_posts = """# Posts Instagram — {nome}
1. Post: 3 erros comuns
2. Reels: como resolver em 30s
3. Carrossel: checklist rápido
4. Post: dica prática
5. Reels: case rápido
6. Carrossel: passo a passo
7. Post: mito ou verdade
8. Reels: resultado real
9. Carrossel: erros fatais
10. Post: comece hoje
"""

seo_articles_sumario = """# Artigos SEO — {nome}
1. Guia completo de {nome} no litoral
2. Como aplicar {nome} no litoral
3. Erros comuns em {nome} no litoral
4. Dicas práticas de {nome}
5. Resultados reais de {nome}
6. Ferramentas para {nome}
7. Checklist de {nome}
8. ROI de {nome}
9. Como começar em {nome}
10. Perguntas frequentes sobre {nome}
"""

webinar = """# Roteiro de Webinar — {nome}
1. Abertura: dor do público
2. Case: primeiro resultado
3. Método: 3 passos
4. Prova social
5. Oferta e bônus
6. Perguntas frequentes
7. Chamada para ação
"""

youtube = """# Roteiro YouTube — {nome}
1. Introdução: promessa
2. Erro comum
3. Método simplificado
4. Exemplo prático
5. Resultado
6. CTA para curso
"""

meta_ads = """# Meta Ads — {nome}
Público: 25 a 55 anos, interesse em {nome}, litoral
Objetivo: leads
Formato: vídeo + carrossel
Orçamento sugerido: R$ 40 a R$ 120/dia
CTAs: Baixar guia, Quero o curso, Quero participar
"""

google_ads = """# Google Ads — {nome}
Palavras: {nome} no litoral, como fazer {nome}, litoral
Tipo: busca + display
CTAs: Baixar guia, Ver curso, Quero aprender
"""

instagram_marketing = """# Posts Instagram — {nome}
1. Post: dica rápida
2. Reels: passo a passo
3. Carrossel: erros comuns
4. Post: case real
5. Reels: resultado
6. Carrossel: checklist
7. Post: mito ou verdade
8. Reels: antes/depois
9. Carrossel: comece agora
10. Post: pergunte nos comentários
"""

reels = """# Reels — {nome}
1. Roteiro: dica em 30s
2. Roteiro: erro comum
3. Roteiro: passo a passo
4. Roteiro: resultado real
5. Roteiro: comece hoje
"""

tiktok = """# TikTok — {nome}
1. Roteiro: dica rápida
2. Roteiro: erro comum
3. Roteiro: passo a passo
4. Roteiro: resultado real
5. Roteiro: comece hoje
"""

shorts = """# Shorts — {nome}
1. Roteiro: dica em 1 minuto
2. Roteiro: erro comum
3. Roteiro: passo a passo
4. Roteiro: resultado real
5. Roteiro: comece hoje
"""

faq = """# FAQ — {nome}
1. Em quanto tempo vejo resultado? De 30 a 60 dias.
2. Preciso investir muito? Não.
3. Funciona para qualquer caso? Na maioria.
4. E se errar? Ajuste rápido.
5. Vale a pena? Sim.
6. Preciso de ferramentas? Não obrigatoriamente.
7. Como medir sucesso? Indicadores.
8. Posso aplicar sozinho? Pode.
9. E se eu não tiver experiência? O curso ensina.
10. Qual o primeiro passo? Defina objetivo.
"""

vendas_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{nome} — Página de Vendas</title>
  <meta name="description" content="Curso completo de {nome} no litoral.">
  <link rel="canonical" href="https://praia.digital/education/cursos/{slug}/vendas.html">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Course",
    "name": "{nome}",
    "description": "Curso completo de {nome} no litoral.",
    "provider": {{"@type":"Organization","name":"Praia Digital","url":"https://praia.digital/"}},
    "url": "https://praia.digital/education/cursos/{slug}/vendas.html"
  }}
  </script>
  <style>
    body{{font-family:'Segoe UI',system-ui,sans-serif;background:#0b1220;color:#e8ecf1;margin:0;padding:0}}
    .wrap{{max-width:960px;margin:0 auto;padding:28px 22px}}
    header nav a{{color:#cfe3ff;text-decoration:none;margin-right:14px;font-weight:500}}
    h1{{font-size:2rem;margin:0 0 .5rem}}
    .lead{{opacity:.85;line-height:1.6;margin-bottom:1rem}}
    .cta{{background:#00B4D8;color:#fff;padding:.7rem 1.2rem;border-radius:999px;font-weight:700;text-decoration:none;display:inline-block;margin-top:.6rem}}
    .grid{{display:grid;gap:1rem;margin-top:1.2rem}}
    .card{{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:18px 20px}}
    .price{{font-size:1.6rem;font-weight:800;color:#90E0EF}}
    footer{{margin-top:22px;opacity:.6;font-size:12px}}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <nav aria-label="Navegação principal">
        <a href="https://praia.digital/index.html">Início</a>
        <a href="https://praia.digital/servicos.html">Serviços</a>
        <a href="https://praia.digital/education/index.html">Academy</a>
      </nav>
    </header>

    <main id="main">
      <h1>{nome}</h1>
      <p class="lead">Curso completo de {nome} no litoral.</p>

      <div class="card">
        <p><strong>Nível:</strong> Iniciante → Intermediário</p>
        <p><strong>Carga horária:</strong> 4 horas</p>
        <p><strong>Acesso:</strong> vitalício + atualizações</p>
        <p class="price">R$ 297</p>
        <a class="cta" href="https://wa.me/5511954346288?text=Quero%20o%20curso%20{nome_slug}">Quero garantir minha vaga</a>
      </div>

      <div class="grid">
        <div class="card">
          <h3>O que você vai aprender</h3>
          <p>Método prático aplicado ao litoral.</p>
        </div>
        <div class="card">
          <h3>Para quem é</h3>
          <p>Para proprietários, investidores e corretores.</p>
        </div>
        <div class="card">
          <h3>Garantia</h3>
          <p>7 dias para testar. Se não gostar, devolvemos 100% do valor.</p>
        </div>
      </div>
    </main>

    <footer>Praia Digital Academy — educação aplicada ao mercado imobiliário do litoral.</footer>
  </div>
</body>
</html>
"""

def slugify(text):
    return text.lower().replace(' ', '-').replace(',', '').replace('!', '').replace('?', '')

count = 0
for curso in cursos_incompletos:
    root = os.path.join(base, curso)
    os.makedirs(root, exist_ok=True)

    for d in required_dirs:
        os.makedirs(os.path.join(root, d), exist_ok=True)

    nome = curso.replace('-', ' ').title()

    # conteúdo dos arquivos
    files = {
        'curso-completo/ficha-completa.md': ficha_completa.format(nome=nome),
        'curso-completo/sumario.md': sumario.format(nome=nome),
        'curso-completo/modulo-1.md': modulo.format(modulo=1, titulo='Fundamentos', nome=nome),
        'curso-completo/modulo-2.md': modulo.format(modulo=2, titulo='Método', nome=nome),
        'curso-completo/modulo-3.md': modulo.format(modulo=3, titulo='Execução', nome=nome),
        'curso-completo/modulo-4.md': modulo.format(modulo=4, titulo='Resultado', nome=nome),
        'checklists/checklist-cadastro.md': checklist_cadastro.format(nome=nome),
        'planilhas/planilha-precificacao.md': planilha_precificacao.format(nome=nome),
        'avaliacao/avaliacao-final.md': avaliacao_final.format(nome=nome),
        'certificado/certificado.md': certificado.format(nome=nome),
        'ebook/lead-magnet.md': ebook_lead_magnet.format(nome=nome),
        'mini-curso/sumario.md': mini_curso_sumario.format(nome=nome),
        'email-sequence/sequencia.md': email_sequence.format(nome=nome),
        'instagram/posts.md': instagram_posts.format(nome=nome),
        'seo-articles/sumario.md': seo_articles_sumario.format(nome=nome),
        'marketing/webinar.md': webinar.format(nome=nome),
        'marketing/youtube.md': youtube.format(nome=nome),
        'marketing/meta-ads.md': meta_ads.format(nome=nome),
        'marketing/google-ads.md': google_ads.format(nome=nome),
        'marketing/instagram-posts.md': instagram_marketing.format(nome=nome),
        'marketing/reels.md': reels.format(nome=nome),
        'marketing/tiktok.md': tiktok.format(nome=nome),
        'marketing/shorts.md': shorts.format(nome=nome),
        'marketing/faq.md': faq.format(nome=nome),
        'vendas.html': vendas_html.format(nome=nome, slug=curso, nome_slug=slugify(nome)),
    }

    for rel, content in files.items():
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1

print(f'Cursos corrigidos: {len(cursos_incompletos)}')
print(f'Arquivos criados: {count}')
