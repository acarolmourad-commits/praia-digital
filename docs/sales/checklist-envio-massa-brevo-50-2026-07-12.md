# Checklist de Envio Manual em Massa — Brevo
**Data alvo:** 2026-07-12  
**Lote:** 50 leads realistas  
**CSV:** `docs/sales/csv-lotes-email/lote-brevo-50-realistas-2026-07-12.csv`

---

## Passo a passo rápido
1. Acesse o Brevo e vá em **Contatos > Importar contatos**.
2. Escolha **Importar de arquivo CSV**.
3. Faça upload de `docs/sales/csv-lotes-email/lote-brevo-50-realistas-2026-07-12.csv`.
4. Mapeie:
   - `email` → E-mail
   - `nome` → Nome
   - `imobiliaria` → Empresa
   - `cidade` → Cidade
   - `whatsapp` → Telefone
   - `link_email_personalizado` → campo personalizado `LINK_EMAIL`
5. Clique em **Confirmar importação**.
6. Crie uma campanha de e-mail com assunto **"Proposta de parceria — Praia Digital"**.
7. Use como remetente: comercial@praia.digital
8. Cole o template de `outreach/emails-personalizados/lead-001-*.html` como corpo HTML.
9. Dispare para a lista importada.

---

## Acompanhamento recomendado
- A cada 10 envios, salve uma captura de tela como evidência.
- Registre respostas em `docs/sales/classificador-respostas-leads-praia-digital-2026.html`.
- Para follow-up D3, use `docs/sales/followup-registro.md`.

---

## Links úteis
- Ferramentas gratuitas: https://praia.digital
- Site oficial: https://acarolmourad-commits.github.io/praia-digital/
