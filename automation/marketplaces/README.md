# Automação — Gestão de Marketplaces (Shopee / TikTok Shop)

Scripts da operação de gestão de lojas (projeto Zion/Praia Digital, reunião 23/09/2026).

## Scripts

| Script | Função | Entrada | Saída |
|---|---|---|---|
| `ofertas_relampago.py` | Recomendador diário de trocas nas ofertas relâmpago (máx. 20 vagas) | Export CSV de produtos/vendas do Upseller | Lista "tirar X / colocar Y" |
| `relatorio_cliente.py` | Gera resumo de desempenho para envio ao cliente | Export CSV de vendas do Upseller | Texto pronto p/ e-mail/WhatsApp |
| `monitor_lojas.py` | Dashboard semáforo 🟢🟡🔴 de todas as lojas | CSVs consolidados (vendas, ads, penalidades) | Tabela de status + alertas |

## Como usar

```bash
python ofertas_relampago.py vendas_30dias.csv --loja "Loja do Rafael"
python relatorio_cliente.py vendas_30dias.csv --loja "Loja do Rafael" --periodo "01/09 a 30/09"
python monitor_lojas.py pasta_com_csvs/
```

## Formato esperado do CSV (export do Upseller)

Colunas mínimas (nomes flexíveis, ver `--help` de cada script):

- `produto` — nome do produto
- `vendas` — unidades vendidas no período
- `receita` — receita no período (R$)
- `estoque` — estoque atual
- `em_oferta_relampago` — 1/0 (opcional; se ausente, usa lista em `config.json`)

## Agendamento

Sugestão: rodar diariamente às 21h (após fechamento das vendas do dia) via cron/Task Scheduler, ou GitHub Actions com os CSVs atualizados na pasta `data/`.
