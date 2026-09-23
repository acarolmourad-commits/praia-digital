# Pipeline B2B Simplificado

Consolida 24 scripts por segmento em 6 parametrizados.

## Antes (24 scripts)
`sanitize_lote_<seg>.py` (7x) + `agendar_followup_<seg>.py` (9x) + `disparar_lote_<seg>.py` (7x)
+ `notificar_*.py` (2x, executava duplicado) + trackers separados por segmento.

## Depois (6 scripts)
| Script | Uso |
|---|---|
| `sanitize_lote.py --segmento X` | Sanitiza lote do segmento (dedup por email/whatsapp) |
| `disparar_lote.py --segmento X` | Gera CSVs WhatsApp/Brevo + checklist e **atualiza last_contact no tracker-master** |
| `agendar_followup.py --segmento X --dias 3` | Agenda follow-ups |
| `notificar.py --mensagem "..."` | Telegram unico (requer TELEGRAM_TOKEN e TELEGRAM_CHAT_ID) |
| `relatorio_diario.py` | Relatorio HTML consolidado do tracker-master |
| `triagem_leads.py --aplicar` | Triagem unica dos 600 leads estagnados |

## Correcoes desta refatoracao
1. **last_contact nunca era atualizado** -> todos os 600 leads apareciam como follow-up 7d (587).
   `disparar_lote.py` agora grava last_contact e status `msg1_enviada` no `tracker-master.csv`.
2. **`parceria_fechada` entrava na fila de follow-up** (101 leads) -> `automacao_diaria.py` agora
   exclui `parceria_fechada`, `arquivado` e `descartado`.
3. **`notificar_vendas_b2b.py` rodava 2x por dia** -> substituido por `notificar.py` unico.
4. **Telegram nao configurado** -> `notificar.py` le `TELEGRAM_TOKEN`/`TELEGRAM_CHAT_ID` do ambiente.
5. **Trackers separados por segmento** -> consolidados em `docs/sales/csv-lotes-b2b/tracker-master.csv`.

## Migracao dos cronjobs
Substituir as chamadas antigas por:
```bat
python scripts\pipeline\sanitize_lote.py --segmento automacao
python scripts\pipeline\disparar_lote.py --segmento automacao
python scripts\pipeline\agendar_followup.py --segmento automacao
python scripts\pipeline\notificar.py --mensagem "Lote automacao pronto"
python scripts\pipeline\relatorio_diario.py
```
Repetir para os segmentos: captacao, proptech, descricao, seo-local, consultoria, avaliacao,
prospeccao (apos recriar o lote de entrada), consultoria_proptech.

## Pendente na maquina local (fora do repo)
- Recriar `lote-b2b-prospeccao-*.csv` (arquivo de entrada ausente -> causa dos [SKIP])
- Rodar `triagem_leads.py --aplicar` uma vez
- Configurar TELEGRAM_TOKEN e TELEGRAM_CHAT_ID
