# Academy — Pré-Deploy Local
Status: ready to merge after Render/DNS activation  
Data: 2026-08-08

## 1) Estrutura verificada
- 64 cursos com `index.html`, `vendas.html` e pastas de conteúdo
- Cada curso com: `curso-completo/`, `checklists/`, `ebook/`, `email-sequence/`, `materiais/`, `imagens/`, `planilhas/`, `avaliacao/`
- Área do aluno: login, dashboard, curso, progresso, certificado
- Backend: FastAPI + SQLAlchemy, 20 testes locais passing

## 2) Fluxo de compra implementado
- `/academy/checkout` cria matrícula + payment `pending`
- Sem Mercado Pago: retorna checkout local `/education/checkout.html?order_id=...`
- Com Mercado Pago: cria preferência e redireciona para `init_point`
- `/academy/checkout/confirm?order_id=` ativa matrícula
- Webhook Mercado Pago: `/academy/payments/mercadopago/webhook`
- E-mail: `/automation/email-confirmation/{enrollment_id}`
- WhatsApp: `/automation/whatsapp-notify/{enrollment_id}`

## 3) Hotmart-ready
- Campos `hotmart_link` no editorial JSON
- Frontend: botão "Comprar agora" e link WhatsApp
- Backend: rota de webhook genérica preparada para receber postback Hotmart

## 4) Checklist produção
- [ ] Render web service criado no workspace correto
- [ ] Banco Postgres `academy-db` provisionado
- [ ] Variáveis de ambiente configuradas
- [ ] Custom domain `academy.praia.digital` apontado
- [ ] `https://academy.praia.digital/health` retornando OK
- [ ] `https://academy.praia.digital/docs` acessível
- [ ] Testes de produção: `/auth/register`, `/leads`, `/checkout`
- [ ] SMTP configurado para e-mails de matrícula
- [ ] Mercado Pago ou Hotmart configurado
- [ ] WhatsApp Business API configurada
