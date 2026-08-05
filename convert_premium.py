import os
from pathlib import Path

cursos = [
    ('aumentar-rentabilidade', 'Como Aumentar em 30% a Rentabilidade', 'Aumente a rentabilidade dos seus imóveis no litoral em até 30% com método', 'R$ 297', '6 horas', 'identificar perdas ocultas, aplicar ganhos rápidos e escalar rentabilidade no litoral'),
    ('especialista-venda-imoveis-litoral', 'Especialista em Venda de Imóveis no Litoral', 'Venda mais imóveis no litoral com método, técnicas de captação e fechamento profissional', 'R$ 397', '8 horas', 'captar leads, negociar e vender imóveis no litoral com autoridade'),
    ('captacao-exclusividade', 'Captação e Exclusividade para Corretores', 'Capture imóveis exclusivos no litoral e feche mais contratos de representação', 'R$ 347', '7 horas', 'captação de imóveis, exclusividade e funil de vendas para corretores'),
    ('marketing-imobiliario', 'Marketing Imobiliário para Corretores', 'Use marketing digital para captar leads, vender mais e se destacar no mercado imobiliário', 'R$ 347', '7 horas', 'marketing digital, captação de leads e posicionamento para corretores'),
    ('analise-de-rentabilidade', 'Análise de Rentabilidade', 'Analise investimentos imobiliários com método e decisão baseada em dados', 'R$ 197', '4 horas', 'análise de rentabilidade, ROI e decisão de investimento'),
    ('automacao-comercial', 'Automação Comercial para Corretores', 'Automatize o funil de vendas, atendimento e follow-up para vender mais com menos esforço', 'R$ 297', '6 horas', 'automação comercial, CRM, follow-up e escala para corretores'),
    ('avaliacao-de-imoveis', 'Avaliação de Imóveis', 'Avalie imóveis no litoral com método, comparáveis e precificação correta', 'R$ 247', '5 horas', 'avaliação de imóveis, comparáveis e precificação no litoral'),
    ('casa-ou-apartamento', 'Casa ou Apartamento no Litoral', 'Escolha entre casa e apartamento no litoral com critérios claros de custo, manutenção e retorno', 'R$ 197', '4 horas', 'escolha entre casa e apartamento, análise de custo e retorno'),
    ('comprar-com-seguranca', 'Comprar com Segurança no Litoral', 'Compre imóveis no litoral evitando golpes, documentação irregular e riscos ocultos', 'R$ 297', '6 horas', 'compra segura, verificação documental e mitigação de riscos'),
    ('comprar-imovel-praia-sem-golpes', 'Comprar Imóvel na Praia Sem Golpes', 'Evite golpes e armadilhas na compra de imóveis na praia com checklist e método', 'R$ 247', '5 horas', 'compra segura na praia, identificação de golpes e verificação documental'),
    ('crm-para-corretores', 'CRM para Corretores', 'Use CRM para organizar leads, follow-up e vendas no mercado imobiliário', 'R$ 247', '5 horas', 'CRM, organização de leads, follow-up e conversão'),
    ('documentacao-imobiliaria', 'Documentação Imobiliária', 'Domine a documentação de imóveis no litoral para comprar, vender e alugar com segurança', 'R$ 247', '5 horas', 'documentação imobiliária, matrícula, certidões e segurança'),
    ('financiamento-imobiliario', 'Financiamento Imobiliário', 'Entenda financiamento, entrada, FGTS e condições para comprar imóveis no litoral', 'R$ 247', '5 horas', 'financiamento, entrada, FGTS e condições de compra'),
    ('flipping', 'Flipping de Imóveis no Litoral', 'Compre, reforme e venda imóveis no litoral com lucro e método', 'R$ 347', '7 horas', 'flipping, reforma, precificação e venda rápida'),
    ('funil-de-vendas', 'Funil de Vendas para Corretores', 'Monte um funil de vendas imobiliário que capta, qualifica e converte leads', 'R$ 297', '6 horas', 'funil de vendas, leads, qualificação e conversão'),
    ('guia-investidor-imobiliario', 'Guia do Investidor Imobiliário', 'Guia completo para investir em imóveis no litoral com segurança e rentabilidade', 'R$ 297', '6 horas', 'investimento imobiliário, escolha, documentação e rentabilidade'),
    ('ia-para-corretores', 'IA para Corretores', 'Use IA para captar leads, criar conteúdo e vender mais imóveis no litoral', 'R$ 297', '6 horas', 'IA aplicada a corretores, conteúdo, leads e atendimento'),
    ('ia-para-imobiliarias', 'IA para Imobiliárias', 'Implemente IA na imobiliária para automatizar operações, marketing e atendimento', 'R$ 347', '7 horas', 'IA para imobiliárias, automação, marketing e gestão'),
    ('imoveis-para-airbnb', 'Imóveis para Airbnb no Litoral', 'Escolha, prepare e posicione imóveis para Airbnb no litoral com alta ocupação', 'R$ 247', '5 horas', 'escolha de imóvel para Airbnb, preparo e posicionamento'),
    ('instagram-para-corretores', 'Instagram para Corretores', 'Use Instagram para captar leads, construir autoridade e vender mais imóveis', 'R$ 247', '5 horas', 'Instagram, conteúdo, leads e autoridade para corretores'),
    ('multiplique-patrimonio', 'Multiplique Patrimônio no Litoral', 'Estratégias para multiplicar patrimônio com imóveis no litoral ao longo do tempo', 'R$ 297', '6 horas', 'multiplicação de patrimônio, estratégia e longo prazo'),
    ('primeiro-imovel-litoral', 'Primeiro Imóvel no Litoral', 'Compre seu primeiro imóvel no litoral com segurança, método e sem dor de cabeça', 'R$ 247', '5 horas', 'primeira compra, segurança, documentação e escolha'),
    ('ptam-na-pratica', 'PTAM na Prática', 'Use o PTAM para avaliação e decisão de investimento em imóveis no litoral', 'R$ 197', '4 horas', 'PTAM, avaliação, decisão e investimento'),
    ('whatsapp-que-vende', 'WhatsApp que Vende no Litoral', 'Use WhatsApp para captar leads, atender e vender imóveis no litoral com método', 'R$ 247', '5 horas', 'WhatsApp, atendimento, follow-up e vendas'),
]

base_root = 'education/cursos'

for slug, nome, promise, price, hours, objetivo in cursos:
    base = f'{base_root}/{slug}'
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

    Path(base, 'curso-completo', 'ficha-completa.md').write_text(f'''# Curso: {nome}
## Nome Comercial
**{nome}: Método Prático para {objetivo.capitalize()}**

## Subtítulo
Do diagnóstico ao resultado: aprenda a aplicar método, evitar erros e crescer no mercado imobiliário do litoral.

## Promessa Principal
Em até 30 dias, você será capaz de aplicar um método prático para {objetivo}.

## Público-alvo
- Proprietários de imóveis no litoral
- Investidores que querem aumentar retorno
- Corretores que querem se especializar
- Interesse: imóveis, litoral, investimento, temporada, rentabilidade

## Pré-requisitos
Nenhum. Curso completo do zero ao resultado.

## Nível
Iniciante → Intermediário

## Tempo Estimado
{hours} de aulas
Total: {hours}

## Valor Sugerido
Curso completo: {price}
À vista: {price.replace('R$ ', 'R$ ')}
Parcelado: 12x de R$ {str(round(int(price.replace('R$ ', '').replace(',', ''))/12, 2)).replace('.', ',')}
Mini curso: R$ 147
E-book: R$ 19,90

## Oferta Principal
- Acesso vitalício + atualizações
- Checklist do curso
- Planilha de acompanhamento
- Modelos prontos
- Comunidade fechada
- Certificado

## Headline
**"{promise}"**

## Big Idea
Resultados no litoral dependem de método, dados e execução consistente.

## Oferta
- **Curso completo:** {price}
- **Mini curso:** R$ 147
- **E-book:** R$ 19,90

## Avatar
**Nome:** Carlos / Fernanda
**Idade:** 25 a 55 anos
**Renda:** R$ 3k a R$ 20k/mês
**Objetivo:** {objetivo}
**Dificuldades:** falta de método, insegurança, resultado baixo
**Desejos:** crescimento, tranquilidade, autoridade

## Dores
- Falta de método
- Insegurança
- Resultado baixo
- Falta de clareza
- Tempo limitado

## Desejos
- Crescimento
- Tranquilidade
- Autoridade
- Previsibilidade
- Resultado

## Objeções
- "Não compensa"
- "É complicado"
- "Não tenho tempo"
- "Vou errar"
- "Não funciona"

## Transformação
- Método aplicado
- Resultado crescente
- Decisão orientada por dados
- Operação profissional
- Tranquilidade

## Programa Completo
### Módulo 1 — Fundamentos
Aula 1.1 — Contexto e oportunidades
Aula 1.2 — Perfil e objetivos
Aula 1.3 — Métricas e metas
Exercício: diagnóstico

### Módulo 2 — Aplicação Prática
Aula 2.1 — Passo a passo prático
Aula 2.2 — Exemplos reais
Aula 2.3 — Erros comuns
Exercício: aplicação

### Módulo 3 — Estratégia
Aula 3.1 — Planejamento
Aula 3.2 — Decisão e priorização
Aula 3.3 — Execução
Exercício: plano

### Módulo 4 — Crescimento
Aula 4.1 — Acompanhamento
Aula 4.2 — Ajustes
Aula 4.3 — Escala
Exercício: escala

## Carga Horária
{hours}

## Material Complementar
- Checklist
- Planilha
- Modelos
- PDFs por módulo
- Comunidade fechada
- Atualizações

## Checklists
- Checklist de diagnóstico
- Checklist de aplicação
- Checklist de estratégia
- Checklist de escala

## Planilhas
- Planilha de acompanhamento
- Planilha de métricas
- Planilha de ROI

## Modelos Prontos
- Modelo de relatório
- Modelo de proposta
- Modelo de revisão

## Scripts
- Script de atendimento
- Script de negociação

## Prompt de IA
Prompt para gerar análises e planos.

## Exercícios
- Exercício 1: diagnóstico
- Exercício 2: aplicação
- Exercício 3: plano
- Exercício 4: escala

## Avaliações
Quiz 20 perguntas
Prova prática: aplicação do método

## FAQ
1. Preciso de experiência? Não.
2. Em quanto tempo vejo resultado? De 15 a 30 dias.
3. Vale a pena? Sim.
4. E se errar? Ajuste com método.
5. Tem suporte? Sim.

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
"Aplique o método agora."

## Upsell
- Mentoria individual: R$ 1.500
- Acompanhamento: R$ 2.800

## Downsell
- Mini curso: R$ 147
- E-book: R$ 19,90

## Cross-sell
- Cursos complementares Praia Digital
''', encoding='utf-8')

    Path(base, 'curso-completo', 'sumario.md').write_text(f'''# Sumário do Curso: {nome}
- Módulo 1: Fundamentos
- Módulo 2: Aplicação Prática
- Módulo 3: Estratégia
- Módulo 4: Crescimento
''', encoding='utf-8')

    Path(base, 'curso-completo', 'modulo-1.md').write_text(f'''# Módulo 1 — Fundamentos

## Introdução
Entenda o contexto, o seu perfil e as métricas essenciais para {objetivo}.

## Aula 1.1 — Contexto e oportunidades
- Mercado atual
- Oportunidades no litoral
- Particularidades regionais

**Exemplo real:** Profissional identificou oportunidade em região em crescimento e aumentou resultado em 25%.

## Aula 1.2 — Perfil e objetivos
- Perfil do aluno
- Objetivos claros
- Metas realistas

## Aula 1.3 — Métricas e metas
- Métricas essenciais
- Metas de curto, médio e longo prazo
- Revisão

## Exercício
Faça o diagnóstico do seu cenário atual.

## Resumo
- Contexto orienta decisão
- Perfil evita erros
- Métricas medem resultado

## Checklist
- [ ] Cenário mapeado
- [ ] Objetivos definidos
- [ ] Métricas escolhidas
- [ ] Metas traçadas

## Materiais para download
- PDF do módulo
- Planilha de diagnóstico

## Ferramentas recomendadas
- Planilha
- Indicadores
- Consultas locais

## Prompt de IA
"Atue como especialista em {objetivo}. Faça um diagnóstico com base nestas respostas: [insira suas respostas]."
''', encoding='utf-8')

    Path(base, 'curso-completo', 'modulo-2.md').write_text(f'''# Módulo 2 — Aplicação Prática

## Introdução
Aplique o método na prática com exemplos reais e evite erros comuns.

## Aula 2.1 — Passo a passo prático
- Etapas claras
- Ação imediata
- Verificação de resultado

**Exemplo real:** Profissional aplicou o passo a passo e obteve ganhos rápidos em 15 dias.

## Aula 2.2 — Exemplos reais
- Caso 1
- Caso 2
- Lições aplicáveis

**Estudo de caso:** Aplicação prática gerou aumento mensurável em 30 dias.

## Aula 2.3 — Erros comuns
- Erro 1
- Erro 2
- Erro 3
- Como evitar

## Exercício
Aplique o método em um cenário real.

## Resumo
- Passo a passo reduz risco
- Exemplos aceleram aprendizado
- Erros evitados poupam tempo

## Checklist
- [ ] Passos executados
- [ ] Resultados verificados
- [ ] Ajustes aplicados

## Materiais para download
- PDF do módulo
- Checklist de aplicação

## Ferramentas recomendadas
- Planilha de acompanhamento
- App de gestão

## Prompt de IA
"Atue como especialista prático. Monte um plano de aplicação para este cenário: [dados]."
''', encoding='utf-8')

    Path(base, 'curso-completo', 'modulo-3.md').write_text(f'''# Módulo 3 — Estratégia

## Introdução
Planeje, decida e priorize ações para crescer com consistência.

## Aula 3.1 — Planejamento
- Objetivos
- Ações
- Prazos
- Recursos

**Exemplo real:** Planejamento simples permitiu crescer sem surpresas.

## Aula 3.2 — Decisão e priorização
- Critérios de decisão
- Priorização
- Risco

**Estudo de caso:** Decisão baseada em dados evitou prejuízo e aumentou retorno.

## Aula 3.3 — Execução
- Rotina
- Acompanhamento
- Ajuste rápido

## Exercício
Monte um plano estratégico para os próximos 30 dias.

## Resumo
- Planejamento evita desperdício
- Decisão orientada reduz risco
- Execução gera resultado

## Checklist
- [ ] Plano definido
- [ ] Ações listadas
- [ ] Prazo estabelecido

## Materiais para download
- PDF do módulo
- Modelo de plano

## Ferramentas recomendadas
- Planner
- Planilha
- App de metas

## Prompt de IA
"Atue como estrategista. Monte um plano prático para este objetivo: [dados]."
''', encoding='utf-8')

    Path(base, 'curso-completo', 'modulo-4.md').write_text(f'''# Módulo 4 — Crescimento

## Introdução
Acompanhe resultados, ajuste estratégias e escale sem perder controle.

## Aula 4.1 — Acompanhamento
- Métricas
- Frequência
- Formato
- Aprendizado

**Exemplo real:** Acompanhamento semanal permitiu ajustes rápidos e crescimento contínuo.

## Aula 4.2 — Ajustes
- Quando ajustar
- Como ajustar
- Validação

**Estudo de caso:** Ajustes pontuais aumentaram resultado sem aumentar esforço.

## Aula 4.3 — Escala
- Processos
- Fornecedores/parcerias
- Crescimento gradual

## Exercício
Monte um plano de escala sustentada.

## Resumo
- Acompanhamento mantém direção
- Ajustes preservam resultado
- Escala depende de processo

## Checklist
- [ ] Métricas revisadas
- [ ] Ajustes aplicados
- [ ] Escala planejada

## Materiais para download
- PDF do módulo
- Planilha de acompanhamento

## Ferramentas recomendadas
- Dashboard
- Planilha
- Sistema de gestão

## Prompt de IA
"Atue como especialista em crescimento. Monte um plano de escala para este cenário: [dados]."
''', encoding='utf-8')

    Path(base, 'checklists', 'checklist-curso.md').write_text(f'''# Checklist — {nome}
- [ ] Diagnóstico realizado
- [ ] Objetivos definidos
- [ ] Aplicação executada
- [ ] Estratégia traçada
- [ ] Escala planejada
''', encoding='utf-8')

    Path(base, 'planilhas', 'planilha-acompanhamento.md').write_text(f'''# Planilha — {nome}
- [ ] Data
- [ ] Ação
- [ ] Resultado
- [ ] Ajuste
- [ ] Status
''', encoding='utf-8')

    Path(base, 'avaliacao', 'avaliacao-final.md').write_text(f'''# Avaliação Final — {nome}
## Quiz
- 20 perguntas sobre fundamentos, aplicação, estratégia e crescimento.

## Prova Prática
- Aplicação do método em cenário real.

## Critério de Aprovação
- 70% no quiz + prova prática aprovada pelo mentor.
''', encoding='utf-8')

    Path(base, 'certificado', 'certificado.md').write_text(f'''# Certificado — {nome}
Modelo: Praia Digital Academy
Curso: {nome}
Carga horária: {hours}
Aprovado: [nome]
Data: [data]
Código: [código único]
''', encoding='utf-8')

    Path(base, 'ebook', 'lead-magnet.md').write_text(f'''# E-book Derivado — {nome}
Título: Guia Rápido para {nome.split(':')[0].strip()}
Formato: PDF 20 a 30 páginas
Preço: gratuito ou R$ 19,90
Conteúdo: checklist, planilha, dicas rápidas.
''', encoding='utf-8')

    Path(base, 'mini-curso', 'sumario.md').write_text(f'''# Mini Curso — {nome}
## Aula 1 — Fundamentos (8 min)
## Aula 2 — Aplicação prática (12 min)
## Aula 3 — Estratégia (10 min)
## Bônus — Planilha de acompanhamento
''', encoding='utf-8')

    Path(base, 'email-sequence', 'sequencia.md').write_text(f'''# Sequência de E-mails — {nome}
## E-mail 1 — Entrega do lead magnet
Assunto: Guia Rápido de {nome.split(':')[0].strip()} (PDF + planilha)
Conteúdo: acesso ao material + introdução ao curso completo
CTA: Quero o curso completo

## E-mail 2 — Case
Assunto: Case: resultado prático
Conteúdo: passo a passo real
CTA: Ver curso completo

## E-mail 3 — Objeção
Assunto: "{nome.split(':')[0].strip()} dá trabalho?"
Conteúdo: quebra de objeção com método
CTA: Começar agora

## E-mail 4 — Prova social
Assunto: Aluno obteve resultado em 30 dias
Conteúdo: depoimento + resultado
CTA: Participar do próximo lote

## E-mail 5 — Urgência
Assunto: Últimas vagas com bônus
Conteúdo: oferta limitada
CTA: Garantir minha vaga
''', encoding='utf-8')

    Path(base, 'instagram', 'posts.md').write_text('''# Posts Instagram — ''' + nome + '''
1. Post: dica prática
2. Reels: passo a passo rápido
3. Carrossel: checklist
4. Post: erro comum
5. Reels: dica de aplicação
6. Carrossel: exemplo real
7. Post: resultado rápido
8. Reels: case prático
9. Carrossel: métrica importante
10. Reels: ajuste simples
11. Post: estratégia básica
12. Carrossel: 5 passos
13. Post: crescimento sem segredo
14. Reels: dúvida comum
15. Carrossel: ferramenta útil
16. Post: comece hoje
17. Reels: case de resultado
18. Carrossel: revisão semanal
19. Post: mito vs verdade
20. Reels: método resumido
''', encoding='utf-8')

    Path(base, 'seo-articles', 'sumario.md').write_text('''# Artigos SEO — ''' + nome + '''
1. ''' + nome + ''' em 2026: guia completo
2. Como aplicar ''' + nome.split(':')[0].strip() + ''' no litoral
3. Guia prático para iniciantes
4. Erros comuns e como evitar
5. Métricas essenciais
6. Resultados reais e casos
7. Ferramentas úteis
8. Checklist essencial
9. Perguntas frequentes
10. Próximos passos
''', encoding='utf-8')

    Path(base, 'marketing', 'webinar.md').write_text('''# Roteiro de Webinar — ''' + nome + '''
1. Abertura: dor do público
2. Case: resultado prático
3. Método: 4 passos
4. Prova social
5. Oferta e bônus
6. Perguntas frequentes
7. Chamada para ação
''', encoding='utf-8')

    Path(base, 'marketing', 'youtube.md').write_text('''# Roteiro YouTube — ''' + nome + '''
1. Introdução: promessa
2. Erro comum
3. Método simplificado
4. Exemplo prático
5. Resultado
6. CTA para curso
''', encoding='utf-8')

    Path(base, 'marketing', 'meta-ads.md').write_text(f'''# Meta Ads — {nome}
Público: 25 a 55 anos, interesse em imóveis, litoral, investimento
Objetivo: leads
Formato: vídeo + carrossel
Orçamento sugerido: R$ 40 a R$ 120/dia
CTAs: Baixar guia, Quero o curso, Quero participar
''', encoding='utf-8')

    Path(base, 'marketing', 'google-ads.md').write_text(f'''# Google Ads — {nome}
Palavras: {slug.replace('-', ' ')}, litoral, imóveis, investimento
Tipo: busca + display
CTAs: Baixar guia, Ver curso, Quero aprender
''', encoding='utf-8')

    Path(base, 'marketing', 'instagram-posts.md').write_text('''# Posts Instagram — ''' + nome + '''
1. Post: dica prática
2. Reels: passo a passo
3. Carrossel: checklist
4. Post: erro comum
5. Reels: case rápido
6. Carrossel: ferramenta
7. Post: resultado
8. Reels: ajuste simples
9. Carrossel: métrica
10. Post: comece hoje
''', encoding='utf-8')

    Path(base, 'marketing', 'reels.md').write_text('''# Reels — ''' + nome + '''
1. Roteiro: dica rápida
2. Roteiro: passo a passo
3. Roteiro: erro comum
4. Roteiro: case rápido
5. Roteiro: resultado
''', encoding='utf-8')

    Path(base, 'marketing', 'tiktok.md').write_text('''# TikTok — ''' + nome + '''
1. Roteiro: dica rápida
2. Roteiro: 1 método, 2 resultados
3. Roteiro: como aplicar
4. Roteiro: resultado rápido
5. Roteiro: case prático
''', encoding='utf-8')

    Path(base, 'marketing', 'shorts.md').write_text('''# Shorts — ''' + nome + '''
1. Roteiro: dica rápida
2. Roteiro: regra simples
3. Roteiro: resultado em 1 minuto
4. Roteiro: ajuste simples
5. Roteiro: case curto
''', encoding='utf-8')

    Path(base, 'marketing', 'faq.md').write_text(f'''# FAQ — {nome}
1. Preciso de experiência? Não.
2. Em quanto tempo vejo resultado? De 15 a 30 dias.
3. Vale a pena? Sim.
4. E se errar? Ajuste com método.
5. Tem suporte? Sim.
6. Como medir sucesso? Métricas claras.
7. Preciso de ferramentas? Ajuda.
8. Funciona para qualquer imóvel? Com método, sim.
9. Como começar? Aplicação prática.
10. Qual o primeiro passo? Diagnóstico.
''', encoding='utf-8')

    Path(base, 'vendas.html').write_text(f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{nome} — Página de Vendas</title>
  <meta name="description" content="{promise}.">
  <link rel="canonical" href="https://praia.digital/education/cursos/{slug}/vendas.html">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Course",
    "name": "{nome}",
    "description": "{promise}.",
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
      <p class="lead">{promise}.</p>
      <div class="card">
        <p><strong>Nível:</strong> Iniciante → Intermediário</p>
        <p><strong>Carga horária:</strong> {hours}</p>
        <p><strong>Acesso:</strong> vitalício + atualizações</p>
        <p class="price">{price}</p>
        <a class="cta" href="https://wa.me/5511954346288?text=Quero%20{slug.replace('-', '%20')}">Quero garantir minha vaga</a>
      </div>
      <div class="grid">
        <div class="card">
          <h3>O que você vai aprender</h3>
          <p>Método prático com aplicação direta no litoral.</p>
        </div>
        <div class="card">
          <h3>Para quem é</h3>
          <p>Para proprietários, investidores e corretores que querem resultado.</p>
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

    print('Gerado:', nome)

print('Concluído:', len(cursos), 'cursos')
