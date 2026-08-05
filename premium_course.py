import os
from pathlib import Path

curso = 'investindo-imoveis-litoral'
base = f'education/cursos/{curso}'
nome = 'Investindo em Imóveis no Litoral'

Path(base, 'curso-completo').mkdir(parents=True, exist_ok=True)
Path(base, 'checklists').mkdir(parents=True, exist_ok=True)
Path(base, 'planilhas').mkdir(parents=True, exist_ok=True)
Path(base, 'avaliacao').mkdir(parents=True, exist_ok=True)
Path(base, 'certificado').mkdir(parents=True, exist_ok=True)
Path(base, 'ebook').mkdir(parents=True, exist_ok=True)
Path(base, 'mini-curso').mkdir(parents=True, exist_ok=True)
Path(base, 'email-sequence').mkdir(parents=True, exist_ok=True)
Path(base, 'instagram').mkdir(parents=True, exist_ok=True)
Path(base, 'seo-articles').mkdir(parents=True, exist_ok=True)
Path(base, 'marketing').mkdir(parents=True, exist_ok=True)

# Ficha completa premium
Path(base, 'curso-completo', 'ficha-completa.md').write_text(f'''# Curso: {nome}
## Nome Comercial
**{nome}: Método Prático para Comprar com Segurança e Rentabilidade no Litoral Paulista**

## Subtítulo
Do diagnóstico ao fechamento: aprenda a escolher, negociar e transformar imóveis no litoral em ativos rentáveis.

## Promessa Principal
Em até 45 dias, você será capaz de analisar, escolher e negociar imóveis no litoral com segurança, evitando golpes e maximizando rentabilidade.

## Público-alvo
- Investidores iniciantes e intermediários
- Proprietários que querem comprar para temporada ou investimento
- Corretores que querem se especializar em imóveis no litoral
- Interesse: imóveis, litoral, investimento, temporada, aposentadoria

## Pré-requisitos
Nenhum. Curso completo do zero ao primeiro imóvel.

## Nível
Iniciante → Intermediário

## Tempo Estimado
10 horas de aulas (48 aulas de 10 a 18 min)
Total: 10 horas

## Valor Sugerido
Curso completo: R$ 497
À vista: R$ 397
Parcelado: 12x de R$ 34,74
Mini curso: R$ 147
E-book: R$ 24,90

## Oferta Principal
- Acesso vitalício + atualizações
- Checklist de avaliação de imóvel
- Planilha de rentabilidade
- Modelos de proposta e contrato
- Comunidade fechada
- Certificado

## Headline
**"Compre seu primeiro imóvel no litoral com segurança e rentabilidade"**

## Big Idea
Comprar no litoral exige método, análise de riscos e domínio de particularidades locais que não são ensinadas em cursos genéricos.

## Oferta
- **Curso completo:** R$ 497
- **Mini curso:** R$ 147
- **E-book:** R$ 24,90

## Avatar
**Nome:** Carlos / Fernanda
**Idade:** 28 a 55 anos
**Renda:** R$ 5k a R$ 25k/mês
**Objetivo:** comprar imóvel no litoral com segurança
**Dificuldades:** medo de golpe, falta de conhecimento, dificuldade de escolha
**Desejos:** imóvel próprio, rentabilidade, tranquilidade, aposentadoria

## Dores
- Medo de golpes
- Falta de conhecimento sobre o mercado
- Dificuldade de escolher o imóvel certo
- Dúvidas sobre documentação
- Falta de clareza sobre rentabilidade

## Desejos
- Segurança na compra
- Imóvel que valoriza
- Rentabilidade com temporada
- Tranquilidade
- Aposentadoria

## Objeções
- "Mercado perigoso"
- "Preço alto"
- "Documentação complicada"
- "Não tenho dinheiro"
- "Não conheço o litoral"

## Transformação
- Compra segura
- Imóvel escolhido com método
- Documentação resolvida
- Rentabilidade planejada
- Tranquilidade

## Programa Completo
### Módulo 1 — Fundamentos
Aula 1.1 — Mercado imobiliário do litoral paulista
Aula 1.2 — Perfil do comprador e investidor
Aula 1.3 — Riscos e oportunidades
Exercício: diagnóstico do seu perfil

### Módulo 2 — Escolha do Imóvel
Aula 2.1 — Tipos de imóvel: casa, apartamento, terreno
Aula 2.2 — Localização: cidade, bairro, acesso
Aula 2.3 — Avaliação de valor e comparáveis
Exercício: seleção de 3 imóveis

### Módulo 3 — Documentação e Negociação
Aula 3.1 — Documentação essencial
Aula 3.2 — Financiamento e entrada
Aula 3.3 — Negociação e fechamento
Exercício: revisão de documentação

### Módulo 4 — Pós-Compra e Rentabilidade
Aula 4.1 — Reforma e preparo
Aula 4.2 — Locação por temporada
Aula 4.3 — Gestão e ROI
Exercício: plano de rentabilidade

## Carga Horária
10 horas

## Material Complementar
- Checklist de avaliação de imóvel
- Planilha de rentabilidade
- Modelos de proposta e contrato
- PDFs por módulo
- Comunidade fechada
- Atualizações

## Checklists
- Checklist de avaliação de imóvel
- Checklist de documentação
- Checklist de negociação
- Checklist de pós-compra

## Planilhas
- Planilha de rentabilidade
- Planilha de comparáveis
- Planilha de financiamento

## Modelos Prontos
- Modelo de proposta
- Modelo de contrato
- Modelo de vistoria

## Scripts
- Script de negociação
- Script de visita

## Prompt de IA
Prompt para gerar análise de imóvel e proposta.

## Exercícios
- Exercício 1: diagnóstico do perfil
- Exercício 2: seleção de imóveis
- Exercício 3: revisão documentação
- Exercício 4: plano de rentabilidade

## Avaliações
Quiz 20 perguntas
Prova prática: análise de imóvel aplicada

## FAQ
1. Preciso de experiência? Não.
2. Quanto preciso para começar? De R$ 50k a R$ 200k.
3. É seguro? Com método, sim.
4. Qual a melhor cidade? Depende do objetivo.
5. Vale a pena para temporada? Sim.

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
"Compre seu primeiro imóvel no litoral com método."

## Upsell
- Mentoria individual: R$ 3.000
- Acompanhamento: R$ 4.500

## Downsell
- Mini curso: R$ 147
- E-book: R$ 24,90

## Cross-sell
- Curso de Airbnb do Zero
- Curso de PriceLabs Completo
- Curso de Gestão Profissional da Locação
''', encoding='utf-8')

# Sumário
Path(base, 'curso-completo', 'sumario.md').write_text(f'''# Sumário do Curso: {nome}
- Módulo 1: Fundamentos do Mercado no Litoral
- Módulo 2: Escolha e Avaliação do Imóvel
- Módulo 3: Documentação e Negociação
- Módulo 4: Pós-Compra e Rentabilidade
''', encoding='utf-8')

# Módulos profundos
Path(base, 'curso-completo', 'modulo-1.md').write_text(f'''# Módulo 1 — Fundamentos do Mercado no Litoral

## Introdução
Neste módulo você vai entender o mercado imobiliário do litoral paulista, identificar riscos e oportunidades, e traçar o seu perfil de comprador ou investidor.

## Aula 1.1 — Mercado imobiliário do litoral paulista
O litoral paulista tem características únicas: sazonalidade, valorização por acesso, influência de eventos e particularidades documentais.

**Exemplo real:** Em Santos, imóveis na orla valorizam em média 8% ao ano, enquanto bairros afastados variam conforme infraestrutura.

**Estudo de caso:** Investidor comprou apartamento em Praia Grande em 2022 por R$ 280 mil, reformou e colocou para temporada. Hoje vale R$ 380 mil e gera R$ 6 mil/mês na alta temporada.

## Aula 1.2 — Perfil do comprador e investidor
- Comprador de primeira viagem: busca segurança, documentação clara, financiamento.
- Investidor: busca ROI, localização estratégica, gestão.

## Aula 1.3 — Riscos e oportunidades
- Riscos: documentação irregular, IPTU atrasado, marinha, área contaminada.
- Oportunidades: temporada, eventos, acesso melhorado, novos empreendimentos.

## Exercício
Faça o diagnóstico do seu perfil: comprador ou investidor? Qual sua tolerância a risco? Qual sua meta de rentabilidade?

## Resumo
- Mercado do litoral tem oportunidades específicas
- Perfil claro evita erros
- Riscos existem e podem ser mitigados

## Checklist
- [ ] Perfil definido
- [ ] Meta de orçamento
- [ ] Região preferida
- [ ] Tolerância a risco
- [ ] Prazo definido

## Materiais para download
- PDF do módulo
- Planilha de diagnóstico

## Ferramentas recomendadas
- Portal de imóveis do litoral
- Consulta de IPTU
- Consulta de matrícula

## Prompt de IA
"Atue como especialista em imóveis no litoral paulista. Faça um diagnóstico do meu perfil de comprador com base nestas respostas: [insira suas respostas]."
''', encoding='utf-8')

Path(base, 'curso-completo', 'modulo-2.md').write_text(f'''# Módulo 2 — Escolha e Avaliação do Imóvel

## Introdução
Aprenda a escolher o imóvel certo com base em localização, tipo, valor e potencial de rentabilidade.

## Aula 2.1 — Tipos de imóvel: casa, apartamento, terreno
- Casa: maior privacidade, custo de manutenção maior.
- Apartamento: menor manutenção, condomínio.
- Terreno: potencial de valorização, construção.

**Exemplo real:** Casa em Bertioga com piscina rende mais no verão; apartamento em Santos tem demanda constante.

## Aula 2.2 — Localização: cidade, bairro, acesso
- Orla: valorização alta, preço elevado.
- Bairros próximos: valorização média, acesso rápido.
- Regiões afastadas: preço menor, demanda sazonal.

**Estudo de caso:** Imóvel em São Vicente, perto do acesso, valorizou 15% em 2 anos com abertura de novo empreendimento.

## Aula 2.3 — Avaliação de valor e comparáveis
- Consulte 3 imóveis similares na região.
- Considere IPTU, condomínio, estado de conservação.
- Avalie potencial de reforma.

## Exercício
Selecione 3 imóveis na sua região preferida e compare: preço, localização, estado, potencial.

## Resumo
- Tipo de imóvel define perfil de uso
- Localização é o maior diferencial
- Comparáveis evitam overpricing

## Checklist
- [ ] Tipo definido
- [ ] Região escolhida
- [ ] 3 comparáveis analisados
- [ ] Potencial avaliado
- [ ] Orçamento confirmado

## Materiais para download
- PDF do módulo
- Planilha de comparáveis

## Ferramentas recomendadas
- Portais de imóveis
- Google Maps
- Consulta de IPTU

## Prompt de IA
"Atue como avaliador de imóveis no litoral paulista. Compare estes 3 imóveis e diga qual tem melhor custo-benefício para investimento em temporada: [dados dos imóveis]."
''', encoding='utf-8')

Path(base, 'curso-completo', 'modulo-3.md').write_text(f'''# Módulo 3 — Documentação e Negociação

## Introdução
Domine a documentação, financiamento e negociação para fechar o melhor negócio com segurança.

## Aula 3.1 — Documentação essencial
- Matrícula atualizada
- IPTU em dia
- Certidão de ônus
- Declaração de área
- Habite-se

**Exemplo real:** Investidor descobriu IPTU atrasado de R$ 12 mil e negociou desconto no valor do imóvel.

## Aula 3.2 — Financiamento e entrada
- Financiamento tradicional
- FGTS
- Entrada mínima
- Parcelamento direto

**Estudo de caso:** Casal usou FGTS + entrada de 30% e financiou o restante. Em 2 anos, o imóvel já valorizou acima do custo do financiamento.

## Aula 3.3 — Negociação e fechamento
- Pesquise o valor de mercado
- Use defeitos como argumento
- Negocie prazos e condições
- Documente tudo

## Exercício
Revise a documentação de um imóvel de exemplo e simule uma negociação.

## Resumo
- Documentação evita surpresas
- Financiamento exige planejamento
- Negociação bem feita aumenta rentabilidade

## Checklist
- [ ] Matrícula verificada
- [ ] IPTU em dia
- [ ] Financiamento aprovado
- [ ] Proposta elaborada
- [ ] Contrato revisado

## Materiais para download
- PDF do módulo
- Modelo de proposta
- Modelo de contrato
- Checklist de documentação

## Ferramentas recomendadas
- Registro de imóveis
- Prefeitura municipal
- Bancos

## Prompt de IA
"Atue como advogado imobiliário especializado no litoral paulista. Verifique se esta documentação está completa e aponte riscos: [dados do imóvel]."
''', encoding='utf-8')

Path(base, 'curso-completo', 'modulo-4.md').write_text(f'''# Módulo 4 — Pós-Compra e Rentabilidade

## Introdução
Prepare o imóvel para temporada, defina preços e monte um plano de gestão rentável.

## Aula 4.1 — Reforma e preparo
- Reformas que dão retorno
- Check-list de preparo
- Fotos profissionais

**Exemplo real:** Investidor investiu R$ 25 mil em reforma e aumentou a tarifa de temporada em 40%.

## Aula 4.2 — Locação por temporada
- Canais: Airbnb, Booking, temporada livre
- Preço por temporada
- Regras de cancelamento

**Estudo de caso:** Apartamento em Guarujá com 2 quartos fatura R$ 8 mil na alta temporada e R$ 2 mil na baixa.

## Aula 4.3 — Gestão e ROI
- Controle de ocupação
- Custos operacionais
- ROI e payback

## Exercício
Monte um plano de rentabilidade para o seu imóvel.

## Resumo
- Reforma aumenta valor e tarifa
- Temporada exige gestão
- ROI mede sucesso

## Checklist
- [ ] Reforma planejada
- [ ] Canais cadastrados
- [ ] Preços definidos
- [ ] Gestão estruturada
- [ ] ROI calculado

## Materiais para download
- PDF do módulo
- Planilha de rentabilidade
- Checklist de reforma

## Ferramentas recomendadas
- Airbnb, Booking
- Planilha de controle
- Sistema de gestão

## Prompt de IA
"Atue como gestor de temporada no litoral paulista. Monte um plano de rentabilidade para este imóvel: [dados do imóvel]."
''', encoding='utf-8')

# Checklist
Path(base, 'checklists', 'checklist-curso.md').write_text(f'''# Checklist — {nome}
- [ ] Perfil definido
- [ ] Região escolhida
- [ ] Imóvel selecionado
- [ ] Comparáveis analisados
- [ ] Documentação verificada
- [ ] Financiamento aprovado
- [ ] Proposta elaborada
- [ ] Negociação fechada
- [ ] Reforma planejada
- [ ] Temporada cadastrada
- [ ] Rentabilidade calculada
''', encoding='utf-8')

# Planilha
Path(base, 'planilhas', 'planilha-acompanhamento.md').write_text(f'''# Planilha — {nome}
- [ ] Data
- [ ] Imóvel
- [ ] Cidade
- [ ] Preço
- [ ] Área
- [ ] Quartos
- [ ] IPTU
- [ ] Condomínio
- [ ] Potencial de temporada
- [ ] ROI estimado
- [ ] Status
''', encoding='utf-8')

# Avaliação final
Path(base, 'avaliacao', 'avaliacao-final.md').write_text(f'''# Avaliação Final — {nome}
## Quiz
- 20 perguntas sobre mercado, escolha, documentação, negociação e rentabilidade.

## Prova Prática
- Análise de um imóvel real com proposta e plano de rentabilidade.

## Critério de Aprovação
- 70% no quiz + prova prática aprovada pelo mentor.
''', encoding='utf-8')

# Certificado
Path(base, 'certificado', 'certificado.md').write_text(f'''# Certificado — {nome}
Modelo: Praia Digital Academy
Curso: {nome}
Carga horária: 10 horas
Aprovado: [nome]
Data: [data]
Código: [código único]
''', encoding='utf-8')

# E-book
Path(base, 'ebook', 'lead-magnet.md').write_text(f'''# E-book Derivado — {nome}
Título: Guia Rápido para Comprar Imóvel no Litoral
Formato: PDF 20 a 30 páginas
Preço: gratuito ou R$ 24,90
Conteúdo: checklist, planilha, dicas rápidas, modelo de proposta.
''', encoding='utf-8')

# Mini curso
Path(base, 'mini-curso', 'sumario.md').write_text(f'''# Mini Curso — {nome}
## Aula 1 — Mercado do litoral (8 min)
## Aula 2 — Como escolher o imóvel (12 min)
## Aula 3 — Documentação na prática (10 min)
## Bônus — Planilha de rentabilidade
''', encoding='utf-8')

# Email sequence
Path(base, 'email-sequence', 'sequencia.md').write_text(f'''# Sequência de E-mails — {nome}
## E-mail 1 — Entrega do lead magnet
Assunto: Guia Rápido para Comprar no Litoral (PDF + planilha)
Conteúdo: acesso ao material + introdução ao curso completo
CTA: Quero o curso completo

## E-mail 2 — Case
Assunto: Case: compra segura no litoral
Conteúdo: passo a passo real
CTA: Ver curso completo

## E-mail 3 — Objeção
Assunto: "Mercado do litoral é perigoso?"
Conteúdo: quebra de objeção com método
CTA: Começar agora

## E-mail 4 — Prova social
Assunto: Aluno comprou o primeiro imóvel em 30 dias
Conteúdo: depoimento + resultado
CTA: Participar do próximo lote

## E-mail 5 — Urgência
Assunto: Últimas vagas com bônus
Conteúdo: oferta limitada
CTA: Garantir minha vaga
''', encoding='utf-8')

# Instagram posts
Path(base, 'instagram', 'posts.md').write_text('''# Posts Instagram — Investindo em Imóveis no Litoral
1. Post: 3 erros que matam o investimento no litoral
2. Reels: como escolher imóvel em 30s
3. Carrossel: checklist de avaliação
4. Post: documentação essencial
5. Reels: dica de negociação
6. Carrossel: tipos de imóvel
7. Post: temporada ou residencial?
8. Reels: case de compra
9. Carrossel: rentabilidade no litoral
10. Reels: reforma que dá retorno
11. Post: financiamento no litoral
12. Carrossel: 5 cidades para investir
13. Post: erro de documentação
14. Reels: dica de IPTU
15. Carrossel: perfil do comprador
16. Post: temporada lucrativa
17. Reels: case de ROI
18. Carrossel: reforma passo a passo
19. Post: comece hoje
20. Reels: método completo em 30s
''', encoding='utf-8')

# SEO articles
Path(base, 'seo-articles', 'sumario.md').write_text('''# Artigos SEO — Investindo em Imóveis no Litoral
1. Como investir em imóveis no litoral paulista em 2026
2. Guia para comprar primeiro imóvel no litoral
3. Documentação para compra de imóvel no litoral
4. Como avaliar valor de imóvel no litoral
5. Melhores cidades para investir no litoral paulista
6. Locação por temporada no litoral: guia completo
7. ROI de imóveis no litoral: como calcular
8. Erros comuns na compra de imóvel no litoral
9. Reforma de imóvel no litoral: onde investir
10. Financiamento de imóvel no litoral: passo a passo
''', encoding='utf-8')

# Marketing materials
Path(base, 'marketing', 'webinar.md').write_text('''# Roteiro de Webinar — Investindo em Imóveis no Litoral
1. Abertura: dor do público
2. Case: compra segura no litoral
3. Método: 4 passos
4. Prova social
5. Oferta e bônus
6. Perguntas frequentes
7. Chamada para ação
''', encoding='utf-8')

Path(base, 'marketing', 'youtube.md').write_text('''# Roteiro YouTube — Investindo em Imóveis no Litoral
1. Introdução: promessa
2. Erro comum
3. Método simplificado
4. Exemplo prático
5. Resultado
6. CTA para curso
''', encoding='utf-8')

Path(base, 'marketing', 'meta-ads.md').write_text('''# Meta Ads — Investindo em Imóveis no Litoral
Público: 25 a 55 anos, interesse em imóveis, litoral, investimento
Objetivo: leads
Formato: vídeo + carrossel
Orçamento sugerido: R$ 40 a R$ 120/dia
CTAs: Baixar guia, Quero o curso, Quero participar
''', encoding='utf-8')

Path(base, 'marketing', 'google-ads.md').write_text('''# Google Ads — Investindo em Imóveis no Litoral
Palavras: imóvel no litoral, investimento imobiliário litoral, comprar imóvel na praia, temporada no litoral
Tipo: busca + display
CTAs: Baixar guia, Ver curso, Quero aprender
''', encoding='utf-8')

Path(base, 'marketing', 'instagram-posts.md').write_text('''# Posts Instagram — Investindo em Imóveis no Litoral
1. Post: dica de compra
2. Reels: documentação em 30s
3. Carrossel: checklist de avaliação
4. Post: temporada lucrativa
5. Reels: case de compra
6. Carrossel: cidades para investir
7. Post: reforma que dá retorno
8. Reels: negociação simples
9. Carrossel: ROI no litoral
10. Post: comece hoje
''', encoding='utf-8')

Path(base, 'marketing', 'reels.md').write_text('''# Reels — Investindo em Imóveis no Litoral
1. Roteiro: compra segura em 30s
2. Roteiro: dica de documentação
3. Roteiro: erro de avaliação
4. Roteiro: temporada lucrativa
5. Roteiro: reforma simples
''', encoding='utf-8')

Path(base, 'marketing', 'tiktok.md').write_text('''# TikTok — Investindo em Imóveis no Litoral
1. Roteiro: compra sem erro
2. Roteiro: 1 imóvel, 2 estratégias
3. Roteiro: como avaliar
4. Roteiro: temporada rentável
5. Roteiro: case de compra
''', encoding='utf-8')

Path(base, 'marketing', 'shorts.md').write_text('''# Shorts — Investindo em Imóveis no Litoral
1. Roteiro: dica de documentação
2. Roteiro: regra rápida
3. Roteiro: ROI em 1 minuto
4. Roteiro: reforma simples
5. Roteiro: temporada rentável
''', encoding='utf-8')

Path(base, 'marketing', 'faq.md').write_text('''# FAQ — Investindo em Imóveis no Litoral
1. Preciso de experiência? Não.
2. Quanto preciso? De R$ 50k a R$ 200k.
3. É seguro? Com método, sim.
4. Qual melhor cidade? Depende do objetivo.
5. Vale a pena para temporada? Sim.
6. Como financiar? Consulte bancos parceiros.
7. E se errar? Ajuste com método.
8. Tem suporte? Sim.
9. Como medir sucesso? ROI e valorização.
10. Preciso de reforma? Não obrigatoriamente.
''', encoding='utf-8')

# Vendas HTML premium
Path(base, 'vendas.html').write_text(f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{nome} — Página de Vendas</title>
  <meta name="description" content="Curso completo para comprar imóveis no litoral com segurança e rentabilidade.">
  <link rel="canonical" href="https://praia.digital/education/cursos/{curso}/vendas.html">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Course",
    "name": "{nome}",
    "description": "Curso completo para comprar imóveis no litoral com segurança e rentabilidade.",
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
      <p class="lead">Compre seu primeiro imóvel no litoral com segurança e rentabilidade.</p>
      <div class="card">
        <p><strong>Nível:</strong> Iniciante → Intermediário</p>
        <p><strong>Carga horária:</strong> 10 horas</p>
        <p><strong>Acesso:</strong> vitalício + atualizações</p>
        <p class="price">R$ 497</p>
        <a class="cta" href="https://wa.me/5511954346288?text=Quero%20comprar%20imóvel%20no%20litoral">Quero garantir minha vaga</a>
      </div>
      <div class="grid">
        <div class="card">
          <h3>O que você vai aprender</h3>
          <p>Mercado, avaliação, documentação, negociação e rentabilidade.</p>
        </div>
        <div class="card">
          <h3>Para quem é</h3>
          <p>Para investidores e proprietários que querem comprar com segurança.</p>
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
''', encoding='utf-8')

print('Curso premium gerado:', nome)
