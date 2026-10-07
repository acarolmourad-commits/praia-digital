# Navegação compartilhada — padrão da página inicial

A fonte única é `partials/header.html`: Comprar, Investir, Meu Imóvel,
Profissionais e Inteligência, com os mesmos 24 links de submenu da home e
CTA “Falar com especialista” em `/interesse.html`. O logo aponta para `/`.

## Preparação do site

`python3 scripts/build-navigation.py --report /tmp/navigation-report.json`
aplica o componente estaticamente às páginas HTML públicas antes do upload
no workflow `deploy.yml`. Não cria commits nem publica por conta própria.
O HTML da fonte permanece preservado; o artefato publicado recebe o menu.
Novas páginas HTML completas recebem o padrão automaticamente.

O builder substitui somente cabeçalhos de navegação, remove o marcador
`pd-shared-nav` para não haver uma segunda injeção pelo script legado e
acrescenta CSS/JS isolados (`pd-navigation`). Não altera conteúdo, formulários,
scripts de aplicação, SEO nem rodapé. É idempotente e funciona com links em
subdiretórios. Arquivos de redirecionamento, fragmentos, backups, templates,
administração e backends são excluídos; o relatório lista todos os casos.

`js/shared.js` continua carregado onde já existia, preservando seu comportamento
não relacionado ao cabeçalho (listings, leads e rodapé).

## Comportamento e testes

- Desktop: hover, clique ou teclado nos grupos.
- Até 1080 px: botão Menu e submenus expansíveis.
- Escape e clique externo fecham menus; `aria-expanded` acompanha o estado.
- CSS limitado a `.pd-site-header` para evitar efeitos no restante da página.
- `python3 -m unittest discover -s tests -p 'test_navigation.py' -v`
- `node --check js/pd-navigation.js`

O workflow `navigation-checks.yml` testa o PR e verifica home, Imóveis,
Bertioga, Santos, Guarujá e Praia Grande. Não faz deploy.
Somente um merge posterior em `main` aciona a publicação existente.
