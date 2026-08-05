# Arquitetura Técnica — Praia Digital Academy
**Status:** Proposta para aprovação  
**Objetivo:** Transformar a Praia Digital Academy em plataforma autônoma de venda de cursos  
**Domínio público:** https://praia.digital/education/  
**Backoffice/app:** a definir em Vercel/Railway/Render

---

## 1. Visão geral

A Academy manterá o site público em `praia.digital/education/` como catálogo e vendas. A área do aluno, checkout, admin e automações ficarão em um app separado, com domínio/subdomínio dedicado (ex: `academy.praia.digital` ou `app.praia.digital`).

Fluxo principal:
Visitante → Catálogo → Página de vendas → Checkout → Webhook → Liberação de acesso → Área do aluno → Conclusão → Certificado → Upsell/Cross-sell

---

## 2. Modelo de dados

### 2.1 Coleções/tabelas principais

- `users`
  - `id`, `name`, `email`, `password_hash`, `phone`, `avatar`, `role` (`student|admin|support`), `created_at`, `updated_at`, `last_login_at`, `status` (`active|blocked|deleted`)

- `courses`
  - `id`, `slug`, `title`, `subtitle`, `headline`, `description`, `level`, `duration`, `price`, `currency`, `status` (`draft|published|archived`), `published_at`, `created_at`, `updated_at`

- `modules`
  - `id`, `course_id`, `order`, `title`, `description`, `created_at`, `updated_at`

- `lessons`
  - `id`, `module_id`, `order`, `title`, `content_type` (`text|video|audio|pdf`), `content_url`, `duration_minutes`, `created_at`, `updated_at`

- `enrollments`
  - `id`, `user_id`, `course_id`, `status` (`active|expired|refunded|cancelled`), `access_until`, `source` (`checkout|admin|import`), `created_at`, `updated_at`

- `progress`
  - `id`, `enrollment_id`, `lesson_id`, `status` (`not_started|in_progress|completed`), `completed_at`, `created_at`, `updated_at`

- `payments`
  - `id`, `user_id`, `course_id`, `gateway`, `gateway_payment_id`, `status` (`pending|paid|failed|refunded`), `amount`, `currency`, `paid_at`, `created_at`, `updated_at`

- `orders`
  - `id`, `user_id`, `status` (`open|paid|cancelled|refunded`), `subtotal`, `discount`, `total`, `currency`, `created_at`, `updated_at`

- `order_items`
  - `id`, `order_id`, `course_id`, `price`, `created_at`

- `carts`
  - `id`, `user_id`, `course_id`, `created_at`, `updated_at`

- `certificates`
  - `id`, `user_id`, `course_id`, `code`, `pdf_url`, `issued_at`, `expires_at`

- `upsell_rules`
  - `id`, `trigger_course_id`, `target_course_id`, `priority`, `discount_percent`, `active`, `created_at`, `updated_at`

- `cross_sell_rules`
  - `id`, `trigger_course_id`, `target_course_id`, `priority`, `discount_percent`, `active`, `created_at`, `updated_at`

- `coupons`
  - `id`, `code`, `type` (`percent|fixed`), `value`, `active`, `valid_from`, `valid_to`, `usage_limit`, `usage_count`, `created_at`, `updated_at`

- `email_templates`
  - `id`, `key` (`welcome|payment_confirmation|access_granted|cart_abandoned|upsell|certificate`), `subject`, `body`, `active`, `created_at`, `updated_at`

- `automation_rules`
  - `id`, `event` (`purchase|completion|cart_abandoned|inactive_7d`), `channel` (`email|whatsapp`), `template_id`, `delay_minutes`, `active`, `created_at`, `updated_at`

---

## 3. Autenticação

- Registro com e-mail/senha e verificação por link.
- Login com e-mail/senha.
- Recuperação de senha por e-mail.
- Sessão via JWT ou sessão server-side.
- Middleware de autenticação em rotas protegidas.

---

## 4. Catálogo e páginas públicas

- Manter `education/index.html` e `education/cursos/*/index.html` como catálogo público.
- Páginas de vendas: `education/cursos/*/vendas.html`.
- SEO/marketing: manter estrutura existente e adicionar schema de curso quando aplicável.
- Integração futura com conteúdo dinâmico via API, sem quebrar URLs atuais.

---

## 5. Checkout e pagamento

- Carrinho por usuário: múltiplos cursos.
- Checkout com seleção de gateway.
- Webhook confirma pagamento → cria `payment`, `order`, `order_items`, `enrollment`, dispara e-mail/WhatsApp.
- Regras de liberação:
  - Curso avulso: acesso imediato após pagamento confirmado.
  - Assinatura: acesso enquanto assinatura estiver ativa.

---

## 6. Área do aluno

- Dashboard: cursos matriculados, progresso geral, certificados, próximas aulas.
- Player de curso:
  - Lista de módulos e aulas.
  - Marcar aula como concluída.
  - Barra de progresso do curso.
  - Acesso a materiais para download.
- Certificado:
  - Emissão automática após conclusão.
  - PDF gerado dinamicamente com nome, curso, data, código de validação.

---

## 7. Painel administrativo

- Gestão de cursos, módulos e aulas.
- Gestão de usuários e matrículas.
- Visualização de pedidos, pagamentos e certificados.
- Suporte: visualização de histórico do aluno e matrículas.
- Relatórios básicos: vendas, conversão, conclusão.

---

## 8. Automação

### 8.1 E-mail
- Templates para:
  - Boas-vindas
  - Confirmação de pagamento
  - Liberação de acesso
  - Carrinho abandonado
  - Upsell/Cross-sell
  - Conclusão de curso + certificado
- Disparo via SMTP ou serviço transacional.

### 8.2 WhatsApp
- Notificação de compra.
- Suporte e follow-up pós-venda.
- Recuperação de carrinho abandonado.
- Lembretes de curso inativo.

### 8.3 Regras de automação
- Eventos: `purchase`, `completion`, `cart_abandoned`, `inactive_7d`, `upsell_opportunity`.
- Condições e atrasos configuráveis.

---

## 9. Upsell e Cross-sell

- Regras configuráveis por curso.
- Oferta automática após primeira compra.
- Aplicação de desconto configurável.
- Exibição na área do aluno e no checkout.

---

## 10. Recuperação de carrinho

- Carrinho persistente por usuário.
- E-mail/WhatsApp automático em 1h, 24h e 72h.
- Cupom opcional para recuperação.

---

## 11. CRM

- Cadastro de leads via formulário público.
- Histórico de interações: e-mail, WhatsApp, compras, suporte.
- Pipeline simplificado: lead → aluno → cliente recorrente.

---

## 12. Stack técnica sugerida

- **Backend:** Node.js ou Python
- **Banco:** PostgreSQL ou MySQL
- **Armazenamento de assets:** S3 ou storage compatível
- **Frontend:** Next.js ou static site + app separado
- **Pagamento:** Stripe/Mercado Pago/Hotmart/Kiwify
- **E-mail:** SMTP próprio ou Resend/SendGrid
- **WhatsApp:** Meta WhatsApp Business API ou provedor oficial
- **Deploy:** Vercel/Railway/Render para app; GitHub Pages mantido para site público

---

## 13. Dependências técnicas

- Domínio `praia.digital` mantido.
- SSL/HTTPS em todos os subdomínios.
- Variáveis de ambiente para segredos:
  - Banco de dados
  - Gateway de pagamento
  - E-mail
  - WhatsApp
  - Storage

---

## 14. Riscos e decisões pendentes

- Gateway preferido para pagamentos no Brasil.
- Modelo de venda: curso avulso, assinatura ou híbrido.
- Regra de certificado: validade, QR Code, verificação pública.
- CRM nativo ou integração com ferramenta externa.

---

## 15. Próximos passos sugeridos

1. Aprovação da arquitetura acima.
2. Definição de gateway e modelo de venda.
3. Criação do repositório/app da Academy.
4. Implementação da Fase 1 (banco + auth + catálogo).
5. Implementação da Fase 2 (checkout + pagamento).
6. Implementação da Fase 3 (área do aluno + certificado).
7. Implementação da Fase 4 (admin + automações).
8. Implementação da Fase 5 (upsell + cross-sell + relatórios).
9. Migração gradual das páginas públicas para o app, mantendo URLs amigáveis.
