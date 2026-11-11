# Operação editorial do boletim

## Estado do piloto

O boletim público e seu RSS são estáticos. A edição de 11/11/2026 reúne três publicações oficiais de 5 e 6 de novembro, conferidas em 11/11. A edição de 02/11 permanece no arquivo e recebeu uma nota posterior sobre o prazo informado da consulta da orla de Bertioga, sem apagar o texto nem alterar sua data original de revisão. Não se anunciam notícias de hoje nem atualização em tempo real. A assinatura por e-mail permanece desativada; ver `docs/newsletter/ATIVACAO-SEGURA.md`.

## Fluxo de atualização

1. O workflow `bulletin-editorial.yml` prepara diariamente uma fila a partir do estado público da Sentinela. Seu artifact contém apenas fontes públicas; **não é armazenamento privado**. A coleta não revalida a fonte nem publica conteúdo. Pode haver atraso do agendador. O mesmo artifact informa a idade da última revisão editorial e prazos registrados: sinaliza os próximos sete dias e prazos passados sem nota posterior. Esses alertas são cálculos sobre registros salvos, não nova consulta às fontes, e não alteram as páginas.
2. O editor lê a fonte original. Confere data real de publicação, local, escopo, relevância, duplicidade e prazo/evento. Uma mudança de hash não é uma notícia. Registrar indisponibilidade; não substituir falha por conteúdo inventado.
3. Criar `data/boletim/edicoes/AAAA-MM-DD.json` com status `reviewed`, identificação honesta do revisor e horário real de revisão com fuso. Cada item requer fonte HTTPS, data publicada (`AAAA-MM-DD`, sem inventar horário), conferência, categoria, cidade, resumo factual e impacto identificado como análise. O resumo da edição explicita se reúne notícias anteriores. Sem notícia aprovada, `items: []` é válido. Use `deadline` quando houver prazo claro na fonte. Divergência material entre notícia e norma exige verificação adicional; não publicar a condição duvidosa como fato.
4. Executar `python3 scripts/gerar_boletim_diario.py`. O gerador usa somente registros aprovados, preserva datas e recusa revisões futuras. Produz páginas datadas, ponteiro atual, arquivo e RSS; não consulta APIs nem envia email.
5. O gerador inclui a nova página datada em `sitemap-boletim.xml`, anunciado no robots.txt, com a data real; o sitemap principal permanece intacto. Não atualizar indiscriminadamente páginas antigas. Rodar testes e abrir PR. Uma edição gerada em branch não é uma publicação. Revisão e aprovação específica do PR antecedem merge/deploy.
6. Depois de publicar, conferir página, RSS, links/fontes e datas ao vivo. Corrigir a edição com nota visível se um fato mudar; não apagar a trilha editorial nem inventar dias ausentes. Em um item histórico, `updates` registra `noted_at`, `reviewer` e `text`; a revisão original e o `pubDate` do RSS permanecem, enquanto `dateModified` e o sitemap refletem a nota posterior. Não afirmar encerramento de formulário apenas porque a data divulgada passou.

## Critérios

- `published_at` é data da notícia; `checked_at` é verificação da fonte; `reviewed_at` é revisão da edição. Nenhum é substituído pelo relógio do visitante.
- Sem preço, amostra, custos e metodologia, não publicar “abaixo do mercado”, yield ou ranking de valorização. Contagem interna de artigos não mede procura externa.
- IA pode ajudar a organizar/resumir; sua participação é identificada. Não atribuir revisão humana inexistente. Conteúdo crítico exige avaliação editorial adequada.
- Não copiar artigos integrais. Usar paráfrase curta, atribuição e link. Não enviar dados pessoais a fontes, logs, artifacts ou repositório público.
- Alertas rápidos só após validação da fonte e da operação; este piloto não tem SLA de tempo real nem disparos recorrentes.

## Verificações

```sh
python3 -m unittest discover -s tests -p 'test_bulletin.py' -v
python3 -m unittest discover -s tests -p 'test_navigation.py' -v
python3 scripts/validate_sitemap_targets.py
node --check js/boletim.js
node --check assets/js/cta-newsletter.js
node tests/bulletin-browser.cjs
```

O teste de navegador requer Playwright e Chromium instalados; `CHROMIUM_PATH` pode indicar um executável local. Ele não submete formulários, faz envios ou acessa fontes externas. Cobre larguras de 320, 360, 390, 768 e 1280 pixels, filtros, vazio, limpeza repetida, cópia de RSS/fallback, leitura sem JavaScript, menu/Escape e ausência de coleta de e-mail. A frequência de publicação não foi fixada: a rotina diária existente é apenas de validação e preparação. Nada envia e-mail ou publica notícias sem revisão.
