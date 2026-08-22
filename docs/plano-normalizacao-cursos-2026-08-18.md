# Plano de normalização dos 64 cursos

## Estado atual
- 64 cursos inventariados em academy/cursos/
- Estrutura comum: index.html, vendas.html, curso-completo/{modulo-1.md..modulo-4.md,sumario.md,ficha-completa.md,MANIFESTO_DO_CURSO.md}, aulas/sumario.md
- Fallback aplicado em content_delivery.py para módulos em arquivos raiz
- Compatibilidade validada: 27/27 testes verdes
- IDs, slugs, títulos, conteúdo, preços, status preservados

## Objetivo
Preparar plano de normalização estrutural sem executar agora.

## Normalização = ETAPA INDEPENDENTE
- Não misturar com arquitetura de marca
- Não misturar com checkout/financeiro
- Executar somente após autorização explícita
- Executar somente em ambiente com Python desbloqueado

## Plano
1. Inventário detalhado de cada curso
2. Identificação de inconsistências estruturais
3. Definição de estrutura alvo
4. Migração seletiva por curso
5. Validação de compatibilidade
6. Testes de entrega
7. Rollback por curso

## Validações necessárias
- Estrutura de diretórios consistente
- Modulos reconhecidos pelo endpoint
- CourseContentSource registrado
- Conteúdo íntegro
- Testes de compatibilidade verdes

## Dependências
- Autorização humana
- Ambiente com Python desbloqueado
- Testes Academy verdes
- Backup do repositório

## Critérios de sucesso
- 64 cursos com estrutura alvo
- 64 slugs preservados
- 0 cursos alterados em conteúdo
- 0 status comercial alterado
- 27/27 testes verdes após normalização
- Rollback funcional por curso

## Não fazer agora
- Não normalizar fisicamente
- Não alterar conteúdo
- Não alterar slugs
- Não alterar IDs
- Não misturar com outras fases
