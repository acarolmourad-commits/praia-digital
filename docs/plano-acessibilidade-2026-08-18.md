# Plano de acessibilidade — auditoria e correção

## Objetivo
Documentar plano de auditoria e correção de acessibilidade sem executar scripts.

## Classificação

### Automatizável (P0/P1)
- Heading estrutural claramente incorreto
- Labels ausentes quando o campo correspondente é inequívoco
- Alt text de imagens decorativas quando puder ser determinado com segurança
- Atributos técnicos claramente faltantes
- Links/botões sem identificação quando o contexto for inequívoco

### Revisão humana (P1/P2)
- Questões semânticas ambíguas
- Design de contraste/foco
- Navegação mobile
- Leitores de tela
- Ordem de leitura

## Priorização

### P0
- Bloqueios críticos de acessibilidade
- Formulários sem labels
- Imagens sem alt text funcional

### P1
- Melhorias de alto impacto
- Navegação e menu
- Botões e links sem identificação

### P2
- Otimizações secundárias
- Contraste e design
- Mobile e teclado

## Validações necessárias
- Teclado
- Foco
- Contraste
- Formulários
- Navegação
- Mobile
- Leitores de tela quando possível
- HTML semântico

## Não executar agora
- Não corrigir automaticamente sem execução
- Não inventar resultados
- Não alterar produção
