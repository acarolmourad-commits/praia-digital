# Informativos Airbnb e Booking

`informativos-revisados.json` contém o conteúdo editorial, fontes primárias, datas de publicação, limites para o Brasil e sugestões identificadas como análise da Praia Digital. A data de revisão só deve mudar após nova conferência editorial. Não é o horário da coleta automática.

Para renderizar localmente, sem consultar serviços ou alterar o estado do monitor:

```sh
python3 scripts/sentinela_airbnb_booking.py --render-only
python3 -m unittest discover -s tests -p 'test_marketplaces_editorial.py' -v
```

A coleta programada continua a cada seis horas. O monitor mantém registros de links ainda sem revisão, sem apresentar disponibilidade ou impacto como confirmados. Alterações de hash são registradas no relatório, mas não geram notícias. Falha ou bloqueio de uma fonte preserva o histórico anterior e é informado no índice.

As páginas revisadas são geradas novamente a partir do JSON em cada execução, para que a coleta não substitua análises por textos genéricos. Para revisar um registro automático, mantenha seu `file` original no JSON. Os arquivos e as datas históricas de detecção ficam preservados no estado.

Ao alterar a edição revisada, atualize também `sitemap-marketplaces.xml` com os endereços revisados e a data real da revisão. O teste de sitemap verifica a correspondência com o JSON. Links automáticos pendentes não entram nesse mapa editorial.

A Booking Newsroom complementa o Partner Hub. Pesquisa de tendências não deve ser descrita como novo recurso, regra de hospedagem ou previsão de ocupação local. O monitor não envia newsletter, e a publicação de um post não comprova que usuários o receberam.

Publicação: branch e pull request, verificações aprovadas e deploy de `main`, conforme o README do repositório.
