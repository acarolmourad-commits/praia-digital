# Revisão da central de links — 08/10/2026

Preparada somente na branch `fix/links-transparencia-2026-10-08`, a partir de `e6a2c82f8ac6c1a1c03d94522755bfdc724a3823`. Não houve merge, deploy, envio de sitemap ou solicitação de indexação.

## Alterações
- Um único cabeçalho, usando o menu canônico existente e apenas o JS de navegação, sem carregar `shared.js` nesta página.
- O simulador agora aponta ao app de ROI; comparação temporada/anual, hub de apps e atendimento ganham ações explícitas.
- Cadastro explicitamente destinado a corretores com CRECI; proprietários são encaminhados ao atendimento.
- Amazon Brasil: buscas por categorias, sem estrelas, avaliações, rankings ou promessa de entrega/garantia sem fonte.
- Quatro buscas brasileiras sem código de afiliado: a identificação brasileira do programa não foi verificada. Isso desativa a comissão desses quatro links; não inventar ou reutilizar um código de outro mercado. Aviso de transparência explícito e `rel="sponsored noopener noreferrer"`.
- Metadados coerentes, foco visível, link para pular ao conteúdo e sitemap separado `sitemap-links.xml`.

## Validação local
`python3 -m unittest discover -s tests -p 'test_links_page.py' -v`: 7 testes aprovados, incluindo idempotência do build real de navegação.
`node --check js/pd-navigation.js`: aprovado.
Chromium/Playwright local: desktop 1440x1000 e mobile 390x844; menu e tecla Escape, oito cards, um H1/cabeçalho, sem overflow horizontal e sem erros JavaScript. Os testes não enviaram formulários nem efetuaram compras e não comprovam funcionamento dos destinos externos.
21 workflows existentes inspecionados: deploy e IndexNow respondem a push apenas em main ou disparo manual. Nenhum workflow foi alterado ou disparado manualmente.

## Pendências antes/depois da publicação
1. Revisar alterações e obter confirmação específica antes de merge em main, pois isso aciona deploy.
2. Verificar todos os destinos e testar o formulário com dados autorizados; verificar cálculos dos apps separadamente.
3. Verificar conta e identificação Amazon Brasil; se ativar monetização, atualizar links, aviso e testes correspondentes.
4. Após deploy autorizado e confirmação HTTP 200, submeter `https://praia.digital/sitemap-links.xml` no Search Console ou incorporar a URL ao sitemap principal; nenhum desses passos foi executado agora.
5. Fortalecer descoberta com link para a central na homepage/rodapé, em mudança futura revisada; a homepage não foi alterada nesta branch.
6. Solicitar indexação da canonical após publicação por meio da interface Search Console. A API de inspeção somente informa o estado e não solicita indexação. Não há garantia de inclusão no índice.
7. A correção é limitada à central de links; alegações e avisos de guias de terceiros/outros destinos continuam exigindo auditoria própria.
