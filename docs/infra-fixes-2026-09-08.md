# Correções de SEO, HTML e Infraestrutura — praia.digital

Data: 2026-09-08

## 1. `imoveis.html` — correção estrutural do DOM e cache-bust
- **Problema:** `<a id="skip-link">` estava posicionado incorretamente antes da abertura de `<body>`, e faltava `</head>` antes de `<body>`, quebrando a renderização do header compartilhado (`pd-shared-nav`).
- **Ação:**
  - Inserido `</head>` antes de `<body>`.
  - Confirmado que `skip-link` já estava dentro do `<body>` como primeiro filho; hierarquia mantida e validada.
  - Aplicado `?v=3` no CSS do head: `https://praia.digital/css/style.css?v=3`.
  - Sem regras locais `display:none` / `visibility:hidden` ocultando header.
  - Confirmado carregamento de `shared.js` antes de `</body>`.
- **Validação:**
  - `https://praia.digital/imoveis.html?v=3` → HTTP 200 OK
- **Commit:** `41d9929ea`  
  Mensagem: `fix: restaurar DOM em imoveis.html e aplicar cache-bust no CSS`

## 2. `/hub/aluguel-temporada-litoral.html` — correção de 404 e links internos
- **Problema:** HTTP 404 na URL antiga após migração para `/hub/aluguel-temporada-litoral/`.
- **Causa raiz:** Página movida para estrutura de diretório sem redirect; deploy é GitHub Pages, que não processa `_redirects`/`netlify.toml`.
- **Ação:**
  - Criado `/hub/aluguel-temporada-litoral.html` com redirect HTML (`meta http-equiv="refresh"`, `window.location.replace()` e `<link rel="canonical">`) apontando para `/hub/aluguel-temporada-litoral/`.
  - Atualizados 57 arquivos do blog que apontavam para a URL quebrada, substituindo por `/hub/aluguel-temporada-litoral/`.
  - Mantido `_redirects` com regra 301 para compatibilidade futura se o deploy migrar para Netlify.
- **Validação:**
  - `https://praia.digital/hub/aluguel-temporada-litoral.html` → HTTP 200 OK (redirect HTML)
  - `https://praia.digital/hub/aluguel-temporada-litoral/` → HTTP 200 OK
  - Links internos pendentes no código-fonte: 0
- **Commit:** `30f4ce7cb`  
  Mensagem: `fix: atualizar links internos para /hub/aluguel-temporada-litoral/`

## Status consolidado
- Deploy em `main` e validado em produção.
- Nenhuma pendência aberta para os itens acima.
