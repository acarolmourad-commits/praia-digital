import os
import re
from pathlib import Path

base = 'education/cursos'

cursos = sorted([d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))])

mkt_posts = 20
mkt_reels = 20
mkt_emails = 10
seo_articles = 10
mkt_meta = 1
mkt_google = 1
mkt_webinar = 1
mkt_youtube = 1
mkt_instagram = 1
mkt_faq = 1
mkt_tiktok = 1
mkt_shorts = 1

default_publico = 'Proprietários, investidores e corretores do litoral.'
default_prerequisito = 'Nenhum.'
default_nivel = 'Iniciante → Intermediário'
default_carga = '4 horas'
default_valor = 'R$ 297'
default_duracao = '4 semanas'

def slug_to_title(slug):
    return slug.replace('-', ' ').replace('_', ' ').title()

def ensure_dirs(curso):
    dirs = [
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
        'marketing'
    ]
    for d in dirs:
        Path(curso, d).mkdir(parents=True, exist_ok=True)

def read_if_exists(path):
    if os.path.exists(path):
        return Path(path).read_text(encoding='utf-8')
    return ''

def ficha(curso, nome, publico, prerequisito, nivel, carga, valor, duracao):
    return f'''# Curso: {nome}
## Nome Comercial
**{nome}: Conteúdo completo aplicado ao mercado imobiliário do litoral**

## Subtítulo
Conteúdo premium para proprietários, investidores e corretores do litoral.

## Promessa Principal
Aprenda na prática, com método e exemplos reais do litoral.

## Público-alvo
{publico}

## Pré-requisitos
{prerequisito}

## Nível
{nivel}

## Tempo Estimado
{carga} de aulas
Total: {duracao}

## Valor Sugerido
Curso completo: {valor}
À vista: {int(float(valor.replace('R$ ','').replace('.',''))*0.9)}
Parcelado: 12x de R$ {round(float(valor.replace('R$ ','').replace('.',''))/12,2)}
Mini curso: R$ 147
E-book: R$ 19,90

## Oferta Principal
- Acesso vitalício + atualizações
- Material complementar
- Comunidade fechada
- Certificado

## Headline
**"{nome}"**

## Big Idea
Conteúdo premium aplicado ao mercado do litoral.

## Oferta
- **Curso completo:** {valor}
- **Mini curso:** R$ 147
- **E-book:** R$ 19,90

## Avatar
**Nome:** Carlos / Fernanda
**Idade:** 25 a 55 anos
**Renda:** R$ 3k a R$ 20k/mês
**Objetivo:** aprender e aplicar no litoral
**Dificuldades:** falta de método, conteúdo genérico
**Desejos:** resultados rápidos, segurança, previsibilidade

## Dores
- Falta de método
- Conteúdo genérico
- Falta de exemplos locais
- Dúvidas práticas
- Falta de acompanhamento

## Desejos
- Método claro
- Exemplos reais
- Resultados previsíveis
- Segurança
- Autoridade local

## Objeções
- "Muito caro"
- "Não funciona"
- "É complicado"
- "Não tenho tempo"
- "Já tentei"

## Transformação
- Método aplicado
- Resultados previsíveis
- Segurança nas decisões
- Autoridade local
- Crescimento profissional

## Programa Completo
### Módulo 1 — Fundamentos
Aula 1.1 — Introdução ao tema
Aula 1.2 — Conceitos essenciais
Aula 1.3 — Mercado local
Exercício: diagnóstico inicial

### Módulo 2 — Aplicação Prática
Aula 2.1 — Passo a passo
Aula 2.2 — Ferramentas
Aula 2.3 — Automação
Exercício: plano prático

### Módulo 3 — Casos Reais
Aula 3.1 — Estudo de caso 1
Aula 3.2 — Estudo de caso 2
Aula 3.3 — Lições aplicáveis
Exercício: adaptação ao seu contexto

### Módulo 4 — Crescimento
Aula 4.1 — Métricas
Aula 4.2 — Otimização
Aula 4.3 — Escala
Exercício: plano de crescimento

## Carga Horária
{carga}

## Material Complementar
- PDFs por módulo
- Templates
- Comunidade fechada
- Atualizações

## Checklists
- Checklist por módulo

## Planilhas
- Planilha de acompanhamento

## Modelos Prontos
- Modelo aplicável

## Scripts
- Script quando aplicável

## Prompt de IA
Prompt para gerar conteúdo com IA.

## Exercícios
- Exercício 1
- Exercício 2
- Exercício 3

## Avaliações
Quiz 20 perguntas
Prova prática: aplicação do método

## FAQ
1. Como funciona? Método passo a passo.
2. Em quanto tempo vejo resultado? De 30 a 60 dias.
3. Preciso de experiência? Não.
4. Vale a pena? Sim.
5. E se não gostar? 7 dias de garantia.

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
"Aprenda com método aplicado ao litoral."

## Upsell
- Mentoria individual: R$ 2.000
- Acompanhamento: R$ 3.500

## Downsell
- Mini curso: R$ 147
- E-book: R$ 19,90

## Cross-sell
- Outros cursos da Praia Digital Academy
'''

def modulo(n, nome_curso):
    return f'''# Módulo {n} — Conteúdo Premium
## Aula {n}.1 — Introdução ao módulo
Conteúdo: visão geral, objetivo, aplicação prática no litoral.

## Aula {n}.2 — Conceitos aplicados
Conteúdo: fundamentos, exemplos reais, particularidades do litoral.

## Aula {n}.3 — Estudo de caso
Conteúdo: caso real, análise, lições.

## Exercício
Aplicação prática no seu contexto.

## Resumo
Pontos-chave para revisão.

## Checklist
- [ ] Conceitos entendidos
- [ ] Caso analisado
- [ ] Exercício aplicado

## Materiais para download
- PDF do módulo
- Templates
- Planilha

## Ferramentas recomendadas
- Ferramenta 1
- Ferramenta 2
- Ferramenta 3

## Prompt de IA
Prompt para acelerar tarefas deste módulo.
'''

def checklist(curso):
    return f'''# Checklist — {curso}
- [ ] Objetivos definidos
- [ ] Método aplicado
- [ ] Ferramentas configuradas
- [ ] Exercícios realizados
- [ ] Revisão feita
- [ ] Próximo passo definido
'''

def planilha(curso):
    return f'''# Planilha — {curso}
- [ ] Data
- [ ] Ação
- [ ] Resultado
- [ ] Observação
'''

def avaliacao(curso):
    return f'''# Avaliação Final — {curso}
## Quiz
- 20 perguntas sobre o conteúdo completo.

## Prova Prática
- Aplicação do método no seu contexto.

## Critério de Aprovação
- 70% no quiz + prova prática aprovada pelo mentor.
'''

def certificado(curso):
    return f'''# Certificado — {curso}
Modelo: Praia Digital Academy
Curso: {curso}
Aprovado: [nome]
Data: [data]
Código: [código único]
'''

def ebook(curso):
    return f'''# E-book Derivado — {curso}
Título: Guia Rápido sobre {curso}
Formato: PDF 20 a 30 páginas
Preço: gratuito ou R$ 19,90
Conteúdo: resumo, templates, dicas rápidas.
'''

def mini_curso(curso):
    return f'''# Mini Curso — {curso}
## Aula 1 — Visão geral (8 min)
## Aula 2 — Conceitos essenciais (12 min)
## Aula 3 — Aplicação prática (10 min)
## Bônus — Material complementar
'''

def email_seq(curso):
    return f'''# Sequência de E-mails — {curso}
## E-mail 1 — Entrega do lead magnet
Assunto: Guia Rápido sobre {curso} (PDF)
Conteúdo: acesso ao material + introdução ao curso completo
CTA: Quero o curso completo

## E-mail 2 — Case
Assunto: Case prático de {curso}
Conteúdo: passo a passo real
CTA: Ver curso completo

## E-mail 3 — Objeção
Assunto: "{curso} é para mim?"
Conteúdo: quebra de objeção com método
CTA: Começar agora

## E-mail 4 — Prova social
Assunto: Aluno obteve resultado com {curso}
Conteúdo: depoimento + resultado
CTA: Participar do próximo lote

## E-mail 5 — Urgência
Assunto: Últimas vagas com bônus
Conteúdo: oferta limitada
CTA: Garantir minha vaga
'''

def instagram_posts(curso):
    posts = []
    for i in range(1, 21):
        if i % 5 == 1:
            posts.append(f'{i}. Post: dica premium sobre {curso}')
        elif i % 5 == 2:
            posts.append(f'{i}. Reels: resultado em 30s')
        elif i % 5 == 3:
            posts.append(f'{i}. Carrossel: checklist rápido')
        elif i % 5 == 4:
            posts.append(f'{i}. Post: caso real')
        else:
            posts.append(f'{i}. Reels: ferramenta prática')
    return '\n'.join(posts)

def reels_roteiros(curso):
    return '\n'.join([f'{i}. Roteiro: dica premium {i}' for i in range(1, 21)])

def tiktok_roteiros(curso):
    return '\n'.join([f'{i}. Roteiro: case rápido {i}' for i in range(1, 11)])

def shorts_roteiros(curso):
    return '\n'.join([f'{i}. Roteiro: dica em 1 minuto {i}' for i in range(1, 11)])

def webinar(curso):
    return f'''# Roteiro de Webinar — {curso}
1. Abertura: dor do público
2. Case: aplicação prática
3. Método: passo a passo
4. Prova social
5. Oferta e bônus
6. Perguntas frequentes
7. Chamada para ação
'''

def youtube(curso):
    return f'''# Roteiro YouTube — {curso}
1. Introdução: promessa
2. Erro comum
3. Método simplificado
4. Exemplo prático
5. Resultado
6. CTA para curso
'''

def meta_ads(curso):
    return f'''# Meta Ads — {curso}
Público: 25 a 55 anos, interesse no tema, litoral
Objetivo: leads
Formato: vídeo + carrossel
Orçamento sugerido: R$ 40 a R$ 120/dia
CTAs: Baixar guia, Quero o curso, Quero participar
'''

def google_ads(curso):
    return f'''# Google Ads — {curso}
Palavras: {slug_to_title(curso).lower()}, litoral
Tipo: busca + display
CTAs: Baixar guia, Ver curso, Quero aprender
'''

def instagram_posts_mkt(curso):
    return '\n'.join([f'{i}. Post: dica sobre {slug_to_title(curso).lower()}' for i in range(1, 11)])

def faq(curso):
    return f'''# FAQ — {curso}
1. Como funciona? Método passo a passo.
2. Em quanto tempo vejo resultado? De 30 a 60 dias.
3. Preciso de experiência? Não.
4. Vale a pena? Sim.
5. E se não gostar? 7 dias de garantia.
6. Qual o investimento? {default_valor}.
7. Tem suporte? Sim.
8. Como acessar? Plataforma online.
9. Tem certificado? Sim.
10. Posso parcelar? Sim.
'''

def vendas_html(curso, nome, valor):
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{nome} — Página de Vendas</title>
  <meta name="description" content="Curso premium de {nome.lower()} para o litoral.">
  <link rel="canonical" href="https://praia.digital/education/cursos/{curso}/vendas.html">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Course",
    "name": "{nome}",
    "description": "Curso premium de {nome.lower()} para o litoral.",
    "provider": {{"@type":"Organization","name":"Praia Digital","url":"https://praia.digital/"}},
    "url": "https://praia.digital/education/cursos/{curso}/vendas.html"
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
      <p class="lead">Conteúdo premium aplicado ao mercado imobiliário do litoral.</p>
      <div class="card">
        <p><strong>Nível:</strong> {default_nivel}</p>
        <p><strong>Carga horária:</strong> {default_carga}</p>
        <p><strong>Acesso:</strong> vitalício + atualizações</p>
        <p class="price">{valor}</p>
        <a class="cta" href="https://wa.me/5511954346288?text=Quero%20o%20curso%20{curso}">Quero garantir minha vaga</a>
      </div>
      <div class="grid">
        <div class="card">
          <h3>O que você vai aprender</h3>
          <p>Conteúdo premium, exemplos reais e aplicação prática no litoral.</p>
        </div>
        <div class="card">
          <h3>Para quem é</h3>
          <p>Para quem quer resultados previsíveis com método aplicado.</p>
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
'''

def seo_summary(curso, nome):
    return f'''# Artigos SEO — {nome}
1. {nome} em 2026
2. Como aplicar {nome.lower()} no litoral
3. Resultados reais de {nome.lower()}
4. Método passo a passo de {nome.lower()}
5. Erros comuns em {nome.lower()}
6. Ferramentas para {nome.lower()}
7. Cases de {nome.lower()} no litoral
8. Como medir resultado em {nome.lower()}
9. Como começar em {nome.lower()}
10. FAQ sobre {nome.lower()}
'''

def progress(nome, status='Concluído'):
    return f'## {status}\n- {nome}\n'

# Processar cada curso
for curso in cursos:
    path = os.path.join(base, curso)
    ensure_dirs(path)
    nome = slug_to_title(curso)
    publico = default_publico
    prerequisito = default_prerequisito
    nivel = default_nivel
    carga = default_carga
    valor = default_valor
    duracao = default_duracao

    ficha_path = os.path.join(path, 'curso-completo', 'ficha-completa.md')
    existing = read_if_exists(ficha_path)
    if existing:
        m = re.search(r'## Público-alvo\n(.*?)\n## Pré-requisitos', existing, re.S)
        if m:
            publico = m.group(1).strip()
        m = re.search(r'## Pré-requisitos\n(.*?)\n## Nível', existing, re.S)
        if m:
            prerequisito = m.group(1).strip()
        m = re.search(r'## Nível\n(.*?)\n## Tempo Estimado', existing, re.S)
        if m:
            nivel = m.group(1).strip()
        m = re.search(r'## Tempo Estimado\n(.*?)\n## Valor Sugerido', existing, re.S)
        if m:
            carga = m.group(1).strip()
        m = re.search(r'## Valor Sugerido\n(.*?)\n## Oferta Principal', existing, re.S)
        if m:
            valor_raw = m.group(1).strip().splitlines()[0]
            mm = re.search(r'R\$\\s*([0-9\\.]+)', valor_raw)
            valor = f'R$ {mm.group(1)}' if mm else 'R$ 297'
        m = re.search(r'## Promessa Principal\\n(.*?)\\n## Público-alvo', existing, re.S)
        if m:
            promessa = m.group(1).strip()
        else:
            promessa = 'Aprenda na prática, com método e exemplos reais do litoral.'

    Path(ficha_path).write_text(ficha(curso, nome, publico, prerequisito, nivel, carga, valor, duracao), encoding='utf-8')
    Path(path, 'curso-completo', 'sumario.md').write_text(f'# Sumário do Curso: {nome}\n- Módulo 1: Fundamentos\n- Módulo 2: Aplicação Prática\n- Módulo 3: Casos Reais\n- Módulo 4: Crescimento\n', encoding='utf-8')
    Path(path, 'curso-completo', 'modulo-1.md').write_text(modulo(1, nome), encoding='utf-8')
    Path(path, 'curso-completo', 'modulo-2.md').write_text(modulo(2, nome), encoding='utf-8')
    Path(path, 'curso-completo', 'modulo-3.md').write_text(modulo(3, nome), encoding='utf-8')
    Path(path, 'curso-completo', 'modulo-4.md').write_text(modulo(4, nome), encoding='utf-8')
    Path(path, 'checklists', 'checklist-curso.md').write_text(checklist(nome), encoding='utf-8')
    Path(path, 'planilhas', 'planilha-acompanhamento.md').write_text(planilha(nome), encoding='utf-8')
    Path(path, 'avaliacao', 'avaliacao-final.md').write_text(avaliacao(nome), encoding='utf-8')
    Path(path, 'certificado', 'certificado.md').write_text(certificado(nome), encoding='utf-8')
    Path(path, 'ebook', 'lead-magnet.md').write_text(ebook(nome), encoding='utf-8')
    Path(path, 'mini-curso', 'sumario.md').write_text(mini_curso(nome), encoding='utf-8')
    Path(path, 'email-sequence', 'sequencia.md').write_text(email_seq(nome), encoding='utf-8')
    Path(path, 'instagram', 'posts.md').write_text(instagram_posts(curso), encoding='utf-8')
    Path(path, 'seo-articles', 'sumario.md').write_text(seo_summary(curso, nome), encoding='utf-8')
    Path(path, 'marketing', 'webinar.md').write_text(webinar(nome), encoding='utf-8')
    Path(path, 'marketing', 'youtube.md').write_text(youtube(nome), encoding='utf-8')
    Path(path, 'marketing', 'meta-ads.md').write_text(meta_ads(curso), encoding='utf-8')
    Path(path, 'marketing', 'google-ads.md').write_text(google_ads(curso), encoding='utf-8')
    Path(path, 'marketing', 'instagram-posts.md').write_text(instagram_posts_mkt(curso), encoding='utf-8')
    Path(path, 'marketing', 'reels.md').write_text(reels_roteiros(curso), encoding='utf-8')
    Path(path, 'marketing', 'tiktok.md').write_text(tiktok_roteiros(curso), encoding='utf-8')
    Path(path, 'marketing', 'shorts.md').write_text(shorts_roteiros(curso), encoding='utf-8')
    Path(path, 'marketing', 'faq.md').write_text(faq(nome), encoding='utf-8')
    Path(path, 'vendas.html').write_text(vendas_html(curso, nome, valor), encoding='utf-8')

print(f'Processados {len(cursos)} cursos.')
