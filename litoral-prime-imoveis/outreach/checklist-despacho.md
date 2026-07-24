# Checklist de despacho manual — dia de disparo
1) Rode o runner:
   `uv run python scripts/run_vendas_do_dia.py`

2) Valide o CSV do dia antes de enviar:
   `uv run python scripts/validar_pronto_disparo.py`
   - Se houver erros, ajuste o lote antes do envio.

3) Abra o painel de despacho:
   `outreach/despacho.html` via servidor local.

4) Para cada lead:
   - Cheque cidade, tipo e mensagem.
   - Clique em enviar/revezar no WhatsApp.
   - Marque `status=respondido` ou `status=descartado` no CSV.

5) Pós-envio:
   - Salve respostas em `outreach/leads-site.csv`.
   - Agende follow-up em até 72h conforme semelhante resposta.

6) Boas práticas:
   - Sem spam; personalizar nome/cidade.
   - Enviar em horário comercial do Brasil.
   - Se houver >160 contatos, priorizar por estágio.
