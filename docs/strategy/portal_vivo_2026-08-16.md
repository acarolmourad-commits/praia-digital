# Portal vivo e dados atualizados — Praia Digital
Data: 2026-08-16
Status: Planejamento + piloto
D2: SEM IMPACTO

## Infraestrutura existente

### eventuais-litoral-paulista-2026-2027/
- 72 páginas
- Calendário de eventos por cidade
- Categorias: agenda, culturais, carnaval
- Públicas, indexadas, com SEO

### conteudo-periodico/
- 7 páginas
- Indicadores semanais
- Rankings semanais
- Relatórios semanais
- Estudos por cidade
- Oportunidades

### exclusivos/
- 5 páginas
- Rankings exclusivos 2026
- Relatório de mercado 2026
- Estudo por cidade
- Conteúdo recomendado

### ferramentas/
- 18 páginas
- Calculadoras Airbnb
- Calendário de eventos
- Comparadores
- Avaliação de preço
- Assistente virtual

### ia/
- 16 páginas
- IA para atendimento
- IA para avaliação
- IA para captação
- IA para comercial
- IA para conteúdo
- IA para gestão
- IA para imagens
- IA para investidores
- IA para jurídico

## Diagnóstico

### Pontos fortes
1. Base de dados já existe
2. Estrutura de eventos está completa
3. Rankings e indicadores são únicos
4. Ferramentas práticas estão disponíveis
5. IA já tem arquitetura inicial

### Gaps
1. **Sem modelo “agora”**: não há páginas vivas por cidade
2. **Sem documentação de fontes**: números sem fonte claramente citada
3. **Sem frequência definida**: conteúdo periódico sem cronograma claro
4. **Branding misto**: Praia Digital e Litoral Prime misturados
5. **Sem automação**: atualizações manuais, sem pipeline
6. **Sem integração**: eventos, dados e notícias não conversam

## Modelo “Agora” — definição

### Estrutura conceitual
```
/santos-agora
/guaruja-agora
/ubatuba-agora
/maresias-agora
/caraguatatuba-agora
```

### Cada página contém
1. **Notícias recentes** (últimas 48h)
2. **Clima** (previsão 7 dias)
3. **Mar** (ondas, maré)
4. **Eventos** (próximos 7 dias)
5. **Mercado** (indicadores da semana)
6. **Imóveis** (destaques)
7. **Temporada** (ocupação, diária)
8. **Acessos** (trânsito, rodovias)

### Regras
1. Nunca inventar dados
2. Sempre citar fonte
3. Sempre marcar horário da atualização
4. Dados não disponíveis → “Sem informação no momento”
5. Atualização humana obrigatória para notícias
6. Automação apenas para clima/mar/eventos com fonte confiável

## Frequência de atualização

### Tempo real
- Clima: 3h
- Mar: 3h
- Eventos: diário
- Notícias: sob demanda humana
- Acessos: diário

### Diário
- Eventos do dia
- Notícias locais
- Acessos/trânsito

### Semanal
- Indicadores
- Rankings
- Oportunidades

### Mensal
- Estudos de cidade
- Relatórios de mercado
- Análises de tendência

## Fontes de dados

### Confiáveis
1. **Clima**: INMET, CPTEC
2. **Mar**: Marinha do Brasil
3. **Eventos**: Prefeituras, secretarias de turismo
4. **Notícias**: Fontes jornalísticas locais
5. **Mercado**: Dados proprietários + fontes oficiais
6. **Acessos**: DER, concessionárias

### Não inventar
- Dados de mercado sem fonte
- Estatísticas sem origem
- Previsões sem base
- Números não verificados

## Piloto: Santos Agora

### Página
`santos-agora.html`

### Conteúdo
1. Notícias recentes de Santos
2. Clima em Santos
3. Condições do mar em Santos
4. Eventos em Santos (próximos 7 dias)
5. Indicadores de mercado de Santos
6. Imóveis em destaque em Santos
7. Temporada em Santos

### Implementação
- HTML estático inicial
- Dados estáticos com marcação de data/hora
- Integração futura com APIs confiáveis
- Atualização manual assistida

## Arquitetura técnica

### Fases de implementação

#### Fase 1: Manual assistido
- Páginas estáticas com dados fixos
- Atualização por script/cron semanal
- Marcação clara de fonte e data

#### Fase 2: Semiautomática
- Integração com APIs públicas
- Clima: INMET/CPTEC
- Mar: Marinha
- Eventos: feeds de prefeituras
- Notícias: RSS de portais locais

#### Fase 3: Automatizada
- Atualização automática com validação
- Alertas para dados inconsistentes
- Histórico de alterações
- Cache e fallback

## Integração com jornadas

### Cidade Agora → Jornada completa
```
Santos Agora
→ Notícia → Análise → Dados
→ Bairros → Imóveis → Temporada
→ Investimento → Mercado → Oportunidade
```

## Riscos e mitigação

| Risco | Mitigação |
|--------|-----------|
| Dados inventados | Política rigorosa: só fontes oficiais |
| Dados desatualizados | Marcação clara de data/hora |
| Automação sem controle | Revisão humana obrigatória |
| Mistura de branding | Padronizar para Praia Digital |
| Dependência de APIs | Fallback para dados manuais |
| Manutenção custosa | Automatizar apenas o repetitivo |

## Próximos passos

1. Criar piloto `santos-agora.html`
2. Documentar fontes de cada dado
3. Definir cronograma de atualização
4. Padronizar branding
5. Avaliar APIs confiáveis
6. Automatizar apenas clima/mar/eventos
