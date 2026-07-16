# Manual de Operação — Outbound WhatsApp + E-mail (Proprietários Autogestores)

**Praia Digital · litoral de SP**
Público: donos que anunciam sozinhos no Airbnb/Booking. Dor: perdem tempo com limpeza, check-in e precificação errada. Solução: Gestão Completa + Precificação Dinâmica.

> ⚠️ **Restrição do ambiente:** não há SMTP nem API do WhatsApp. O sistema **não envia sozinho**. Ele avisa (via Telegram) o que enviar e quando; o envio real é **copia-e-cola manual** no WhatsApp Business / Brevo / Gmail.

---

## 1. O que já está pronto

- **18 lotes** (149 a 166), **94 leads por canal** = **188 contatos** (WhatsApp + e-mail)
- Cada lead tem 3 mensagens prontas (abordagem → solução/ROI → encerramento)
- Trackers únicos: `tracker-whatsapp-proprietarios.csv` e `tracker-email-proprietarios.csv`
- Dashboards: `dashboard-whatsapp-proprietarios.html`, `dashboard-email-proprietarios.html`, `dashboard-outbound-proprietarios.html` (consolidado)
- Crons automáticos avisam o follow-up de cada dia no Telegram

---

## 2. Rotina diária (5 minutos)

1. **Receba o aviso no Telegram** às 18h (WhatsApp) e 18h30 (e-mail):
   - Lista de leads que devem receber **Msg2/Msg3** (WPP) ou **E2/E3** (e-mail) hoje
2. **Copie a mensagem do CSV** correspondente e envie manualmente:
   - WhatsApp: `docs/sales/csv-lotes-email/lote-whatsapp-proprietarios-<LOTE>-2026-07-15.csv`
   - E-mail: `docs/sales/csv-lotes-email/lote-email-proprietarios-<LOTE>-2026-07-15.csv`
   - Colunas: `Mensagem_1_Abordagem`, `Mensagem_2_Solucao`, `Mensagem_2_5_ProvaROI`, `Mensagem_3_Encerramento` (WPP) / `Email_1_Abordagem`, `Email_2_Solucao`, `Email_3_Encerramento` (e-mail)
3. **Marque o envio** no registro do lote (`outreach/followup-registro-<LOTE>.md` ou `followup-registro-email-<LOTE>.md`) — opcional, o tracker é a fonte real.

---

## 3. Quando um lead responde

### No WhatsApp
- Respondeu "sim" à Msg2 → envie `Mensagem_2_5_ProvaROI` + link `assets/retorno-gestao-completa.html`
- Fechou → envie `Mensagem_4_Onboarding` + link `assets/onboarding-proprietario.html`

### No e-mail
- Respondeu → responda com o caso de ROI (mesma lógica da Msg2.5)
- Fechou → envie o onboarding (mesma landing)

### Registre no tracker (1 comando)
```bash
cd C:/Users/Carolina/praia-digital
# WhatsApp
python scripts/atualizar_status_whatsapp.py --lote 149 --nome "Fernanda Lima" --status respondeu
python scripts/atualizar_status_whatsapp.py --lote 149 --nome "Fernanda Lima" --status fechou --valor 1200
# E-mail
python scripts/atualizar_status_email.py --lote 149 --nome "Fernanda Lima" --status fechou --valor 1200
```
Status válidos: `pendente_email1/msg1 | enviado_* | respondeu | fechou | sem_interesse`

---

## 4. Acompanhar resultados

- **Todo dia:** os crons regeram os dashboards automaticamente. Abra:
  - `docs/sales/dashboard-outbound-proprietarios.html` (visão única)
- **Todo domingo 19h:** recebe no Telegram o **resumo semanal** (ROI por cidade + histórico em `historico-semanal-whatsapp.json`)

---

## 5. Gerar um lote novo (próximo ciclo)

Quando chegar um novo lote Brevo (ex: lote 167):
```bash
cd C:/Users/Carolina/praia-digital
python scripts/gerar_lote_whatsapp.py --lote 167 --data 2026-07-20
python scripts/gerar_lote_email.py   --lote 167 --data 2026-07-20
git add -A && git commit -m "Add: lote 167 outbound" && git push
```
Pronto — o cron passa a avisar o follow-up desse lote automaticamente.

---

## 6. Estrutura de arquivos

```
scripts/
  gerar_lote_whatsapp.py        # gera CSV WPP de um lote
  gerar_lote_email.py           # gera CSV e-mail de um lote
  consolidar_tracker_whatsapp.py / _email.py
  atualizar_status_whatsapp.py  / _email.py
  gerar_dashboard_whatsapp.py   / _email.py / _outbound.py
  cron_whatsapp_diario.py       # 18h: dashboards + aviso WPP
  cron_email_diario.py          # 18h30: aviso e-mail
  resumo_semanal_whatsapp.py    # dom 19h
docs/sales/csv-lotes-email/
  lote-whatsapp-proprietarios-*.csv
  lote-email-proprietarios-*.csv
  tracker-whatsapp-proprietarios.csv
  tracker-email-proprietarios.csv
docs/sales/
  dashboard-whatsapp-proprietarios.html
  dashboard-email-proprietarios.html
  dashboard-outbound-proprietarios.html
outreach/
  template-whatsapp-proprietarios.md
  template-email-proprietarios.md
  material-retorno-msg2.md
  onboarding-proprietario.md
  followup-registro-<LOTE>.md / followup-registro-email-<LOTE>.md
assets/
  retorno-gestao-completa.html
  onboarding-proprietario.html
```

## 7. Comando "one-click" (ativação em massa)

Para marcar o **primeiro envio (Msg1 + Email1)** como feito em todos os lotes de uma vez:
```bash
cd C:/Users/Carolina/praia-digital
python scripts/marcar_primeiro_envio.py
python scripts/executar_outbound.py --push
```
Isso atualiza os trackers e os dashboards, e versiona tudo no repo (GitHub Pages reflete o painel).

Para **refrescar todos os dashboards e versionar** a qualquer momento:
```bash
python scripts/executar_outbound.py --push
```

## 8. Metas do mês

Edite `docs/sales/METAS_OUTBOUND.json` (campos `respondeu`, `fechou`, `receita_estimada`).
O dashboard consolidado (`dashboard-outbound-proprietarios.html`) mostra barras de progresso vs meta.
Exemplo de metas de julho/2026: 28 respostas, 15 fechados, R$ 18.000 de receita estimada.

## 9. Prova de entrega (auditoria)

`python scripts/gerar_prova_entrega.py` (já rodado dentro de `executar_outbound.py --push`) gera:
- `docs/sales/prova-entrega-outbound.json` — log estruturado por lote/canal
- `docs/sales/prova-entrega-outbound.html` — relatório visual de quantos Msg1/E1, Msg2/E2, respostas e fechamentos já ocorreram

Use para auditar: "quais lotes já tiveram o primeiro toque?" e "quantas mensagens foram disparadas?".

## 10. Regras de ouro

- ✅ Sempre copie a mensagem do CSV (já está personalizada com nome e cidade)
- ✅ Marque o status no tracker após cada resposta/fechamento
- ✅ Nunca recrie ativos de ROI/preço — reutilize `assets/roi-ia-imobiliaria.html` etc.
- ❌ Não tente disparo por API/SMTP (não configurado)
- ❌ Não deixe o tracker dessincronizado: os crons já rodam `consolidar_tracker_*` antes dos dashboards

## 11. Disparo B2B — Imobiliárias (Expansão A/C)

O funil B2B é **paralelo** ao de proprietários, com 587 leads armados:
- `docs/sales/csv-lotes-b2b/lote-b2b-reativacao-2026-07-16.csv` (486 imobiliárias em reativação)
- `docs/sales/csv-lotes-b2b/lote-b2b-whitelabel-2026-07-16.csv` (101 parceiras — proposta white-label)

**Para preparar o envio (1 comando):**
```bash
python scripts/preparar_disparo_b2b.py
# gera docs/sales/csv-lotes-b2b/disparo-b2b-consolidado-2026-07-16.csv (587 leads, Msg1 pronta)
```

**Rotina de envio (manual, copia-e-cola ou Brevo/WhatsApp Business):**
1. Abra o CSV consolidado. Cada linha tem `Nome`, `Telefone`, `Msg1`.
2. Envie a `Msg1` pelo WhatsApp (ou importe no Brevo/WhatsApp Business com etiquetas).
3. **Marque como enviado** (one-click):
   ```bash
   python scripts/marcar_primeiro_envio_b2b.py
   ```
   Isso grava `Data_Msg1=hoje` e `Status=enviado_msg1` no `tracker-b2b.csv`.
4. O cron `followup-b2b-imobiliarias` (18h) avisa no Telegram os `Msg2` (D+1) e `Msg3` (D+3).

**Trackers B2B (separados do B2C, não misturar):**
- `docs/sales/csv-lotes-b2b/tracker-b2b.csv` — reativação
- `docs/sales/csv-lotes-b2b/tracker-whitelabel.csv` — leads do widget white-label

**White-label:** a calculadora standalone (`praia.digital/assets/calculadora-widget-standalone.html?tenant=santos-ancora`) captura donos no site da parceira; o lead cai em `tracker-whitelabel.csv` com `parceiro_id`.

## 11b. E-mail B2B (Expansão E — multicanal)

O B2B também tem canal de E-MAIL (paralelo ao WhatsApp), espelhando o funil B2C:
- `scripts/gerar_lote_email_b2b.py --status contato_inicial_enviado` → `lote-email-b2b-reativacao-2026-07-16.csv` (486)
- `scripts/gerar_lote_email_b2b.py --status parceria_fechada --whitelabel` → `lote-email-b2b-whitelabel-2026-07-16.csv` (101)
- Consolidar: `python scripts/consolidar_tracker_email_b2b.py` → `tracker-email-b2b.csv` (isolado do B2C)
- Marcar E1 (após enviar): `python scripts/marcar_primeiro_envio_email_b2b.py`
- Follow-up (cron 18h, Telegram): `followup-email-b2b-imobiliarias` avisa E2 (D+2) / E3 (D+5)

**Tracker B2B isolado:** WPP (`tracker-b2b.csv`) e E-mail (`tracker-email-b2b.csv`) são separados do B2C — não misturar.
