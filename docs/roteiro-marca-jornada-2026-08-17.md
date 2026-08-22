# Roteiro de separação de marca e jornada

## Estado atual
- Marca única: Praia Digital
- Públicos misturados: proprietários, corretores, imobiliárias, investidores, hóspedes
- Jornadas misturadas: serviços padronizados, IA personalizada, Academy, conteúdo editorial
- CTA genérico: WhatsApp como ponto único de avanço

## Arquitetura A — Marca abrangente
Praia Digital
├── Imóveis
├── Temporada
├── Serviços
├── IA para imobiliárias
├── Academy
└── Conteúdo

Páginas afetadas:
- index.html
- servicos.html
- contato.html
- cidades/*
- servicos/*
- education/*
- blog/*

Navegação:
- Mantém estrutura atual
- Adiciona seção “IA para imobiliárias” com destaque

CTAs:
- Separar CTAs por seção
- Manter WhatsApp humano para IA

Públicos:
- Todos mantidos na mesma marca

Intenção:
- Marca forte no litoral
- IA como produto dentro da marca

Riscos:
- Confusão entre serviço padronizado e IA personalizada
- Dificuldade de segmentação automática

Benefícios:
- Menor esforço técnico
- Mantém SEO consolidado

Impacto técnico:
- Baixo; ajustes de conteúdo e navegação

Impacto comercial:
- Médio; pode manter confusão de posicionamento

Migração:
- Não requer migração de domínio
- Apenas ajuste de conteúdo e navegação

## Arquitetura B — Separação por intenção
Praia Digital
├── Imobiliário
│   ├── Imóveis
│   ├── Temporada
│   └── Serviços imobiliários
├── Tecnologia
│   └── IA para imobiliárias
└── Academy
    └── Cursos

Páginas afetadas:
- Cria novas seções/clusters
- Mantém URLs existentes
- Adiciona página dedicada para IA

Navegação:
- Menu com seções separadas
- Breadcrumbs ajustados por cluster

CTAs:
- Serviços padronizados → checkout automático
- IA → WhatsApp humano com briefing

Públicos:
- Proprietários/temporada → Imobiliário
- Corretores/imobiliárias → Tecnologia/IA ou Academy

Intenção:
- Marca de infraestrutura + braço de tecnologia

Riscos:
- Maior complexidade inicial
- Necessidade de validação de marca

Benefícios:
- Clareza comercial
- Automação por perfil
- Melhor SEO por intenção

Impacto técnico:
- Médio; ajustes de navegação, schema, conteúdo

Impacto comercial:
- Alto; separação clara de oferta

Migração:
- Não requer migração de domínio
- Apenas ajuste de estrutura e conteúdo

## Diferenças entre arquiteturas
- Clareza: B > A
- Esforço: A < B
- Automação: B > A
- SEO: B > A
- Manutenção: A > B

## Jornadas identificadas
1. Cliente imobiliário
- VISITA → SERVIÇO → LEAD → PROPOSTA → COBRANÇA → PAGAMENTO → ENTREGA

2. Cliente Academy
- VISITA → CURSO → CHECKOUT → PAGAMENTO_CONFIRMADO → LIBERAÇÃO_AUTOMÁTICA

3. IA para imobiliárias
- VISITA → DIAGNÓSTICO → BRIEFING → PROPOSTA → WHATSAPP HUMANO → NEGOCIAÇÃO → CONTRATAÇÃO → ONBOARDING

## Onde as jornadas se misturam
- Home com cards mistos
- servicos.html sem separação por perfil
- contato.html como único destino final
- blog com links genéricos para servicos.html
- Falta de checkout automático para serviços/Academy

## Decisão necessária
- Escolher arquitetura A ou B
- Autorizar separação de marca
- Autorizar ajuste de navegação
- Autorizar novo conteúdo de IA
