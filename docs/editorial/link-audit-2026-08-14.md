# Relatório de correção de links quebrados — 2026-08-14

## 1. Problema inicial
Links absolutos em `/blog/` usavam prefixo `/blog/` ou `/` que, quando resolvidos a partir do diretório `blog/`, resultavam em caminhos inexistentes.

## 2. Correção aplicada
- **Arquivos reparados:** 2123 HTMLs em `blog/`
- Padrão convertido:
  - `/servicos.html` → `../servicos.html`
  - `/imoveis.html` → `../imoveis.html`
  - `/bairros/index.html` → `../bairros/index.html`
  - `/blog/qualquer-coisa.html` → `qualquer-coisa.html`
  - Demais hubs absolutos do raiz site para `../<destino>`

## 3. Validação pós-correção (somente `blog/`)
- Links quebrados restantes em `blog/`: **1147**
- Principais causas restantes:
  - Destinos que não existem no projeto atual
  - Referências a artigos/nomes de arquivos divergentes
  - Caminhos ambíguos que precisam de decisão editorial

## 4. Casos que exigem decisão humana/editorial
Esses destinos não foram alterados automaticamente:
- `/blog/education/cursos/index.html`
- `/blog/cidades/santos.html`
- `/blog/blog/...`
- Artigos cujo slug real difere do link atual

## 5. Ação recomendada
1. Revisar lista completa de 1147 links quebrados restantes.
2. Para cada caso:
   - Confirmar destino editorial correto, ou
   - Remover link se não houver destino definido.
3. Após ajustes manuais, rodar nova auditoria focalizada.
