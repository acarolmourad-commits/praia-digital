# Estratégia para reduzir revisão humana de links ambíguos

## Problema
- 9.409 links classificados como AMBÍGUO
- Não é seguro corrigir automaticamente todos
- Não é viável revisar todos manualmente

## Objetivo
MINIMIZAR trabalho humano, NÃO zerar os links.

## Estratégia

### 1. Agrupamento por padrão
- Identificar padrões recorrentes nos links ambíguos
- Exemplos:
  - `../servicos.html`
  - `../education/cursos/index.html`
  - `../cidades/santos.html`
  - `../bairros/index.html`
  - `../education/formacoes/captacao-imoveis.html`

### 2. Identificação de regras determinísticas futuras
- Para cada padrão, verificar se há correspondência inequívoca
- Regra só é candidata se:
  - padrão for inequívoco
  - destino correto puder ser comprovado
  - não houver múltiplos destinos plausíveis
  - alteração não mudar intenção comercial
  - não houver risco de redirecionamento semântico

### 3. Validação antes da execução
- Cada regra deve ser testada em dry-run
- Cada candidato deve ser classificado como:
  - APROVÁVEL_AUTOMAÇÃO
  - REVISÃO_HUMANA
- Apenas APROVÁVEL_AUTOMAÇÃO pode ser executado

### 4. Redução gradual
- Começar pelos padrões mais frequentes
- Aplicar somente quando houver evidência suficiente
- Registrar taxa de redução por iteração

## Métricas esperadas
- Total ambíguos: 9.409
- Meta inicial: reduzir para < 3.000 com regras determinísticas
- Restante: revisão humana prioritária por impacto

## Não fazer
- Não tentar zerar os ambíguos
- Não corrigir sem regra validada
- Não misturar ambíguos com determinísticos
