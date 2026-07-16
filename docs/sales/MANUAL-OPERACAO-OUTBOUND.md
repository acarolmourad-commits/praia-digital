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

## 7. Regras de ouro

- ✅ Sempre copie a mensagem do CSV (já está personalizada com nome e cidade)
- ✅ Marque o status no tracker após cada resposta/fechamento
- ✅ Nunca recrie ativos de ROI/preço — reutilize `assets/roi-ia-imobiliaria.html` etc.
- ❌ Não tente disparo por API/SMTP (não configurado)
- ❌ Não deixe o tracker dessincronizado: os crons já rodam `consolidar_tracker_*` antes dos dashboards
