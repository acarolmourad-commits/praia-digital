# IA para Imobiliárias — Arquitetura do Produto
Data: 2026-08-16
Status: Planejamento
D2: SEM IMPACTO

## 1. Auditoria do que já existe

### ia/ — 16 páginas
**Função:** Soluções de IA por segmento
**Status:** REAPROVEITAR
**Páginas:**
- Chat IA
- IA para Atendimento ao Cliente
- IA para Avaliação
- IA para Captação
- IA Comercial
- IA para Produção de Conteúdo
- IA para Gestão
- IA para Imagens
- + 8 páginas complementares

**Avaliação:** Estrutura boa, mas precisa de jornada comercial e conexão com diagnóstico/proposta.

### proptech/ — 4 páginas
**Função:** Posicionamento de tecnologia
**Status:** CONSOLIDAR em ia/ ou servicos/
**Páginas:**
- Startup Proptech
- Proptech startup para imobiliárias
- Plano 7 dias
- Serviços de IA

**Avaliação:** Sobreposto com ia/. Recomendo integrar em ia/ como contexto de tecnologia.

### servicos/ — 63 páginas
**Função:** Serviços comerciais por cidade e tipo
**Status:** MANTER
**Páginas relevantes:**
- Automação Imobiliária
- Consultoria Proptech
- Descrição com IA
- + 60 serviços

**Avaliação:** Base comercial existente. Precisa de conexão com IA como camada superior.

### ferramentas/ — 18 páginas
**Função:** Ferramentas práticas
**Status:** MANTER
**Páginas relevantes:**
- Assistente Virtual para Compradores
- Avaliação de preço
- Calculadoras (diária, limpeza, ocupação)
- Simulador de ROI
- Calendário de eventos

**Avaliação:** Ferramentas úteis que podem alimentar casos de uso de IA.

### ferramentas-gratuitas/ — 32 páginas
**Função:** Lead magnets por cidade
**Status:** MANTER fora do sitemap público
**Avaliação:** Comercial/sistema. Útil para qualificação inicial.

### marketing/ — 14 páginas
**Função:** Conteúdo para redes sociais e campanhas
**Status:** MANTER
**Avaliação:** Pode ser integrado como caso de uso de IA para marketing.

### cases/ — 6 páginas
**Função:** Cases de sucesso
**Status:** AUDITAR
**Páginas:**
- Automação para Imobiliárias
- Fechamento no centro histórico com IA
- Imobiliária Porto da Lua gera 35 leads em 30 dias
- Recomendação automática de imóveis
- Costa Verde reduz tempo de resposta em 60%
- ROI positivo em 90 dias

**Avaliação:** Separar cases reais de demonstrações/exemplos. Nunca apresentar demonstração como resultado real.

### education/ — 181 páginas
**Função:** Academy — cursos para imobiliárias e corretores
**Status:** MANTER
**Avaliação:** Base educacional. Pode alimentar jornada B2B.

### curso/ — 6 páginas
**Função:** Materiais de curso para corretores
**Status:** CONSOLIDAR em education/ ou academy/
**Avaliação:** Sobreposto com education/. Unificar.

### propostas/ — 5 páginas
**Função:** Propostas comerciais
**Status:** MANTER fora do sitemap público
**Páginas:**
- Apresentação para Parceria
- Contrato de Parceria Digital
- Proposta Personalizada — Automação para Imobiliárias
- Proposta Comercial — Serviços de IA
- Proposta Comercial Personalizada

**Avaliação:** Comercial/sistema. Usar após diagnóstico.

### lead/ — 11 páginas
**Função:** Lead magnets por cidade
**Status:** MANTER fora do sitemap público
**Avaliação:** Qualificação inicial. Integrar com diagnóstico.

### landings/ — 11 páginas
**Função:** Landing pages comerciais
**Status:** MANTER fora do sitemap público
**Páginas:**
- Corretores Autônomos
- Imóveis na Costa Verde
- Simulação de Financiamento
- Investidores Seed
- Parcerias — Imobiliárias do Litoral
- + 6 more

**Avaliação:** Comercial/sistema. Usar em campanhas específicas.

### personas/ — 9 páginas
**Função:** Personas de usuário
**Status:** MANTER como referência interna
**Avaliação:** Útil para personalização de conteúdo e IA.

## 2. Definição do produto

### O que é
Agente de IA personalizado para o negócio imobiliário.

### O que não é
- Chatbot genérico
- Ferramenta pronta sem configuração
- Automação sem supervisão humana
- Promessa de resultados garantidos

### O que faz
- Responde perguntas com base no conhecimento da imobiliária
- Apoia atendimento, vendas, locação e temporada
- Aprende com documentos, processos e histórico
- Encaminha casos que precisam de humano
- Organiza informações para decisão

### Como é configurado
- Conhecimento interno: documentos, políticas, processos
- Região: cidade, bairro, característica local
- Tipo de imóvel: apartamento, casa, comercial, temporada
- Público: comprador, inquilino, proprietário, investidor
- Processos: captação, venda, locação, administração
- Tom de voz: formal, próximo, técnico

### Limitações
- Não inventa informações
- Não toma decisões jurídicas ou financeiras
- Não substitui profissionais quando supervisão é necessária
- Não garante volume de leads ou vendas
- Depende de dados de entrada e supervisão humana

### Supervisão humana
- Todo conteúdo gerado por IA deve ser revisado quando publicado
- Atendimento automático deve ter canal humano de fallback
- Decisões comerciais são do cliente, não do agente

## 3. Perfis de cliente

### A. Pequena imobiliária
- Problema: pouca equipe, atendimento lento, conhecimento disperso
- Intenção: automatizar sem perder controle
- Caso de uso: atendimento inicial, qualificação, FAQ
- Nível de personalização: médio
- Potencial comercial: médio
- Objeções: custo, complexidade, medo de perder contato humano

### B. Imobiliária média
- Problema: escala maior, processos repetitivos, múltiplos canais
- Intenção: ganhar eficiência sem aumentar equipe
- Caso de uso: atendimento + vendas + captação
- Nível de personalização: alto
- Potencial comercial: alto
- Objeções: integração com sistemas existentes, treinamento

### C. Grande operação
- Problema: volume alto, consistência, conhecimento compartilhado
- Intenção: padronizar e escalar
- Caso de uso: conhecimento interno, treinamento, atendimento 24h
- Nível de personalização: muito alto
- Potencial comercial: muito alto
- Objeções: segurança, governança, SLA

### D. Corretor autônomo
- Problema: tempo limitado, atendimento fora do horário, conhecimento específico
- Intenção: parecer disponível sem estar conectado 24h
- Caso de uso: atendimento inicial, qualificação, FAQ
- Nível de personalização: médio
- Potencial comercial: baixo-médio
- Objeções: custo, complexidade, medo de parecer robô

### E. Gestor imobiliário
- Problema: múltiplos imóveis, processos repetitivos, documentação
- Intenção: organizar e automatizar gestão
- Caso de uso: conhecimento de imóveis, processos, documentos
- Nível de personalização: alto
- Potencial comercial: médio-alto
- Objeções: integração, dados sensíveis, confiabilidade

### F. Administrador de locação
- Problema: atendimento a inquilinos, manutenção, contratos
- Intenção: responder dúvidas comuns, organizar informações
- Caso de uso: FAQ de locação, processos, documentos
- Nível de personalização: médio
- Potencial comercial: médio
- Objeções: dados sensíveis, supervisão

### G. Gestor de temporada
- Problema: check-in, regras, disponibilidade, hóspedes
- Intenção: automatizar atendimento sem perder experiência
- Caso de uso: dúvidas de hóspedes, regras, disponibilidade
- Nível de personalização: médio-alto
- Potencial comercial: médio
- Objeções: experiência do hóspede, flexibilidade

### H. Empresa de lançamentos
- Problema: alto volume de perguntas, informações repetitivas, qualificação
- Intenção: escalar atendimento sem perder qualidade
- Caso de uso: atendimento inicial, qualificação, FAQ do empreendimento
- Nível de personalização: alto
- Potencial comercial: alto
- Objeções: integração com CRM, consistência da marca

### I. Empresa de avaliação
- Problema: dados de mercado, metodologia, relatórios
- Intenção: organizar conhecimento e apoiar análise
- Caso de uso: conhecimento de mercado, metodologia, comparações
- Nível de personalização: alto
- Potencial comercial: médio-alto
- Objeções: precisão, fontes, atualização

### J. Operação especializada em litoral
- Problema: sazonalidade, temporada, eventos, múltiplos destinos
- Intenção: conhecimento local + automação
- Caso de uso: atendimento em múltiplos idiomas, eventos, temporada
- Nível de personalização: muito alto
- Potencial comercial: alto
- Objeções: conteúdo local, atualização constante

## 4. Casos de uso

### Atendimento
- Responder perguntas frequentes
- Orientar interessados sobre processos
- Encaminhar contatos para humanos
- Responder fora do horário comercial

### Vendas
- Qualificar leads por perfil e orçamento
- Responder dúvidas sobre imóveis
- Apoiar corretores com informações organizadas
- Acompanhar jornada do interessado

### Locação
- Responder dúvidas sobre aluguel
- Explicar documentação necessária
- Orientar sobre contratos
- Apoiar administração

### Temporada
- Responder dúvidas de hóspedes
- Explicar regras e disponibilidade
- Apoiar check-in e check-out
- Gerenciar expectativas

### Conhecimento interno
- Armazenar políticas e processos
- Treinar novos colaboradores
- Responder dúvidas da equipe
- Organizar documentação

### Marketing
- Apoiar criação de conteúdo
- Planejar campanhas
- Organizar informações de imóveis
- Gerar ideias de posts

### Captação
- Apoiar proprietários com perguntas iniciais
- Qualificar leads de captação
- Organizar informações de imóveis
- Encaminhar para especialistas

## 5. Pacotes

### Pacote 1: Atendimento
- Agente de atendimento ao cliente
- FAQ automático
- Encaminhamento para humano
- Relatórios básicos

### Pacote 2: Vendas
- Atendimento + qualificação
- Apoio a corretores
- Organização de informações
- Acompanhamento de leads

### Pacote 3: Locação
- Atendimento + conhecimento de locação
- FAQ de inquilinos
- Apoio a administração
- Documentação básica

### Pacote 4: Temporada
- Atendimento especializado para temporada
- Dúvidas de hóspedes
- Regras e disponibilidade
- Experiência do hóspede

### Pacote 5: Personalizado
- Configurado conforme operação
- Todos os módulos anteriores
- Integração com sistemas existentes
- Supervisão e ajustes contínuos

## 6. Jornada B2B

```
CONTEÚDO
↓
EDUCAÇÃO
↓
PROBLEMA
↓
CASO DE USO
↓
SOLUÇÃO
↓
AGENTE PERSONALIZADO
↓
DIAGNÓSTICO
↓
DEMONSTRAÇÃO
↓
PROPOSTA
↓
IMPLANTAÇÃO
↓
ACOMPANHAMENTO
```

### CTAs por etapa
1. **Conteúdo:** "Saiba mais sobre IA para imobiliárias"
2. **Educação:** "Entenda como funciona"
3. **Problema:** "Descubra se sua imobiliária pode usar IA"
4. **Caso de uso:** "Veja exemplos práticos"
5. **Solução:** "Conheça a solução"
6. **Agente:** "Agente personalizado para seu negócio"
7. **Diagnóstico:** "Solicite um diagnóstico gratuito"
8. **Demonstração:** "Agende uma demonstração"
9. **Proposta:** "Receba uma proposta"
10. **Implantação:** "Comece agora"
11. **Acompanhamento:** "Suporte contínuo"

## 7. Arquitetura de páginas

### Páginas existentes a reaproveitar
- ia/ia-atendimento.html → /solucoes/ia-atendimento/
- ia/ia-comercial.html → /solucoes/ia-vendas/
- ia/ia-avaliacao.html → manter
- ia/ia-captacao.html → manter
- ia/ia-conteudo.html → manter
- servicos/automacao.html → manter
- servicos/consultoria-proptech.html → manter
- ferramentas/assistente-virtual.html → manter
- cases/case-*.html → manter

### Páginas novas necessárias
1. **Página pilar:** /solucoes/ia-para-imobiliarias/
2. **Página de produto:** /solucoes/agente-ia-imobiliaria/
3. **Pacote atendimento:** /solucoes/ia-atendimento/
4. **Pacote vendas:** /solucoes/ia-vendas/
5. **Pacote locação:** /solucoes/ia-locacao/
6. **Pacote temporada:** /solucoes/ia-temporada/
7. **Pacote personalizado:** /solucoes/agente-personalizado/

### Páginas não necessárias agora
- Landing pages comerciais → depois de validação
- Páginas de proposta → sistema, não público
- Páginas de diagnóstico → depois de formulário

## 8. Página pilar

**Título:** IA para Imobiliárias — Agente Personalizado | Praia Digital

**Estrutura:**
1. Hero: o que é, para quem é, CTA "Solicitar diagnóstico"
2. Problemas que resolve
3. Como funciona
4. Casos de uso
5. Personalização
6. Limitações e transparência
7. Segurança e supervisão humana
8. FAQ
9. Próximos passos

**Tom:** Educativo, transparente, sem promessas exageradas.

## 9. Conteúdo educativo

### Cluster editorial
1. IA para imobiliárias
2. Como usar IA em uma imobiliária
3. IA para corretores
4. IA para atendimento imobiliário
5. IA para vendas de imóveis
6. IA para locação
7. IA para temporada
8. Como treinar um agente de IA
9. Agente de IA personalizado
10. IA para conhecimento interno
11. IA para atendimento de proprietários

**Regra:** Cada página deve responder uma necessidade real. Não criar páginas apenas por palavra-chave.

## 10. E-E-A-T e transparência

### O que declarar
- Quem oferece: Praia Digital
- Experiência: portal imobiliário + conteúdo + tecnologia
- Metodologia: configuração personalizada + supervisão humana
- Limitações: explícitas em cada página
- Dados: como são tratados, se aplicável
- Supervisão humana: sempre presente

### O que não fazer
- Inventar clientes
- Inventar resultados
- Inventar integrações
- Prometer automações que não existem

## 11. Cases

### Cases existentes
- Automação para Imobiliárias — verificar se é real
- Fechamento no centro histórico com IA — verificar
- Imobiliária Porto da Lua gera 35 leads — verificar
- Recomendação automática de imóveis — verificar
- Costa Verde reduz tempo de resposta em 60% — verificar
- ROI positivo em 90 dias — verificar

### Classificação
- CASE REAL: cliente verificado, dados reais
- DEMONSTRAÇÃO: cenário simulado
- EXEMPLO HIPOTÉTICO: cenário ilustrativo
- PROTÓTIPO: versão em desenvolvimento

### Regra
Se não houver cases reais, criar seção "Exemplos de aplicação" e não "Resultados de clientes".

## 12. Integração com o portal

### Fluxo natural
```
ARTIGO SOBRE IA
↓
CASO DE USO
↓
SOLUÇÃO
↓
AGENTE PERSONALIZADO
↓
DIAGNÓSTICO
↓
PROPOSTA
```

### Links internos
- blog/ → ia/ → solucoes/
- cases/ → solucoes/
- servicos/ → solucoes/
- ferramentas/ → solucoes/
- education/ → solucoes/
- proprietarios/ → solucoes/

## 13. SEO

### Página pilar
- Intenção: comercial + educativa
- Título: IA para Imobiliárias — Agente Personalizado | Praia Digital
- H1: IA para Imobiliárias
- Meta description: Agente de IA personalizado para imobiliárias, corretores e gestores. Conhecimento, atendimento e automação configurados para sua operação.
- Canonical: /solucoes/ia-para-imobiliarias/
- Schema: BreadcrumbList, FAQPage, Organization
- CTA: "Solicitar diagnóstico"

### Páginas de pacote
- Intenção: comercial
- Título: IA para [Atendimento/Vendas/Locação/Temporada] — Praia Digital
- H1: IA para [Atendimento/Vendas/Locação/Temporada]
- Meta description: [Descrição do pacote]
- Canonical: /solucoes/ia-[atendimento/vendas/locacao/temporada]/
- Schema: BreadcrumbList, FAQPage
- CTA: "Conhecer solução" → /solucoes/agente-personalizado/

## 14. Indexação

### Páginas indexáveis
- /solucoes/ia-para-imobiliarias/ — INDEXÁVEL
- /solucoes/agente-ia-imobiliaria/ — INDEXÁVEL
- /solucoes/ia-atendimento/ — INDEXÁVEL
- /solucoes/ia-vendas/ — INDEXÁVEL
- /solucoes/ia-locacao/ — INDEXÁVEL
- /solucoes/ia-temporada/ — INDEXÁVEL
- /solucoes/agente-personalizado/ — INDEXÁVEL

### Páginas não indexáveis
- /propostas/ — NÃO INDEXÁVEL (comercial/sistema)
- /lead/ — NÃO INDEXÁVEL (comercial/sistema)
- /landings/ — NÃO INDEXÁVEL (comercial/sistema)
- /personas/ — NÃO INDEXÁVEL (interno)

## 15. Segurança e confiança

### Limitações explícitas
- O agente não inventa informações
- O agente não fornece respostas sem base
- O agente não assume decisões jurídicas
- O agente não assume decisões financeiras
- O agente não substitui profissionais quando supervisão for necessária
- O agente não promete resultados comerciais garantidos

### Transparência
- Quando a resposta depender de informação atualizada, indicar a necessidade de fonte ou atualização
- Todo conteúdo gerado por IA deve ser revisado quando publicado
- Atendimento automático deve ter canal humano de fallback
- Decisões comerciais são do cliente, não do agente

## 16. Arquitetura comercial final

### Mapa do produto
```
IA PARA IMOBILIÁRIAS
├── Atendimento
├── Vendas
├── Locação
├── Temporada
└── Personalizado
```

### Mapa dos clientes
```
PEQUENA IMOBILIÁRIA → Atendimento
IMOBILIÁRIA MÉDIA → Vendas + Atendimento
GRANDE OPERAÇÃO → Personalizado
CORRETOR AUTÔNOMO → Atendimento
GESTOR IMOBILIÁRIO → Personalizado
ADMINISTRADOR → Locação
GESTOR TEMPORADA → Temporada
LANÇAMENTOS → Vendas + Personalizado
AVALIAÇÃO → Conhecimento
LITORAL → Personalizado
```

### Mapa dos casos de uso
```
ATENDIMENTO → FAQ, encaminhamento, qualificação
VENDAS → Qualificação, apoio ao corretor, organização
LOCAÇÃO → Dúvidas, documentação, processos
TEMPORADA → Dúvidas de hóspedes, regras, disponibilidade
CONHECIMENTO → Políticas, processos, treinamento
MARKETING → Criação, planejamento, organização
CAPTAÇÃO → Apoio ao proprietário, qualificação
```

### Mapa dos pacotes
```
PACOTE 1: ATENDIMENTO
PACOTE 2: VENDAS
PACOTE 3: LOCAÇÃO
PACOTE 4: TEMPORADA
PACOTE 5: PERSONALIZADO
```

### Mapa das páginas
```
/solucoes/ia-para-imobiliarias/ — Pilar
/solucoes/agente-ia-imobiliaria/ — Produto
/solucoes/ia-atendimento/ — Pacote 1
/solucoes/ia-vendas/ — Pacote 2
/solucoes/ia-locacao/ — Pacote 3
/solucoes/ia-temporada/ — Pacote 4
/solucoes/agente-personalizado/ — Pacote 5
```

### Mapa dos CTAs
```
Conteúdo → "Saiba mais"
Educação → "Entenda como funciona"
Problema → "Descubra se sua imobiliária pode usar IA"
Caso de uso → "Veja exemplos práticos"
Solução → "Conheça a solução"
Agente → "Agente personalizado"
Diagnóstico → "Solicite um diagnóstico"
Demonstração → "Agende uma demonstração"
Proposta → "Receba uma proposta"
```

### Mapa do funil
```
CONTEÚDO
↓
EDUCAÇÃO
↓
PROBLEMA
↓
CASO DE USO
↓
SOLUÇÃO
↓
AGENTE PERSONALIZADO
↓
DIAGNÓSTICO
↓
DEMONSTRAÇÃO
↓
PROPOSTA
↓
IMPLANTAÇÃO
↓
ACOMPANHAMENTO
```

### Mapa dos links internos
```
blog/ → ia/ → solucoes/
cases/ → solucoes/
servicos/ → solucoes/
ferramentas/ → solucoes/
education/ → solucoes/
proprietarios/ → solucoes/
```

## 17. Próximos passos

1. Criar página pilar /solucoes/ia-para-imobiliarias/
2. Auditar cases existentes (real vs demonstração)
3. Criar formulário de diagnóstico
4. Estruturar demonstração
5. Integrar com conteúdo educativo
6. Definir métricas de sucesso
7. Validar com clientes reais antes de escalar

## 18. D2

D2: SEM IMPACTO

Nenhuma alteração em leads, CRM, tracking, automações, mensagens, métricas ou páginas do experimento.
