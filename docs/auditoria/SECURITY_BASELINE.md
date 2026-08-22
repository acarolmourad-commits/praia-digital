# SECURITY BASELINE — PRAIA DIGITAL

Data da auditoria: 2026-08-19
Modo: DISCOVER → AUDIT → EVIDENCE → CLASSIFY → REPORT
Status: apenas auditoria; nenhuma alteração de produção executada.

---

## 1. Status geral

SEGURANÇA: P1 / UNKNOWN

Resumo: o repositório expõe segredos em arquivos de ambiente e o pipeline de deploy permite execução direta de código local sem portas humanas explícitas. A superfície de ataque principal concentra-se em:
- exposição/acidente com `.env`,
- autorização/upload no painel admin e content-delivery,
- webhook de pagamento com caminhos de bypass por configuração ausente,
- orquestrador/cron com execução local ampla,
- monitoração/observabilidade ainda insuficiente para respostas fail-closed.

---

## 2. Resumo executivo

Foram avaliados repositório, CI/CD, API Academy, Academy frontend, Publication Gate, Article Generator, orquestrador, crons, webhooks, banco, conteúdo editorial, backend e superfície de ataque do site.

P0: nenhum achado confirmado como exploração concreta ativa, mas existe risco concreto de publicação não autorizada por bypass do Publication Gate + segredo em `.env` com possibilidade de commit acidental.
P1: webhook de pagamento com bypass por env ausente, painel admin sem rate-limit/brute-force e CORS aberto por padrão.
P2: orquestrador/cron executam push local amplo, falta de MFA, ausência de 2FA, dependências possivelmente sem lockfile, monitoramento parcial.
P3: melhorias de hardening sem evidência de comprometimento imediato.
Unknown: backups testados e restore não testado; deploy em produção indisponível para validação externa direta.

---

## 3. P0

Nenhum P0 confirmado com comprometimento ativo.
P0 potencial preventivo:
- Possibilidade de commit acidental de `.env` com segredos de SMTP/Mercado Pago/Hotmart/WhatsApp/DB → se ocorrer, gera exposição grave e pode habilitar abuso de integrações.
- Possibilidade de bypass do Publication Gate via `article_generator.write_article()` se o módulo falhar em carregar `publication_gate.py` por erro de path/spec, retornando `None`/caminho de escrita alternativa.

---

## 4. P1

| ID | Componente | Achado | Evidência | Severidade | Exploração possível? | Correção recomendada |
|----|------------|--------|-----------|-----------|----------------------|----------------------|
| P1-01 | Secrets | Arquivo `.env` presente na raiz e referenciado; `.env.example` confirma segredos de SMTP, DB, Hotmart, Mercado Pago e WhatsApp. | `.env` não legível para auditoria; `.env.example` lista chaves reais. | P1 | Commit acidental/roubo local pode expor integrações. | Migrar segredos para cofre/github secrets; remover `.env` versionado; pré-commit secret scan. |
| P1-02 | Webhooks | `verify_webhook()` pode retornar `True` quando secret está ausente, inclusive fora de sandbox. | `academy/core/payments/webhooks.py` linhas 30-37, 34-37, 46-49, 55-58. | P1 | Evento forjado se credencial ausente. | Fail-closed: se segredo não configurado, rejeitar webhook com 500/403 e logar alerta. |
| P1-03 | API/CORS | `ALLOWED_ORIGINS` default para `"*"` e `allow_credentials=True`. | `academy/main.py` linhas 22-34. | P1 | CSRF/credential abuse cross-origin. | Restringir CORS a domínios autorizados por ambiente; bloquear `*` em produção. |
| P1-04 | Auth/RateLimit | Rate limit só aplica se `APP_ENV=production`. | `academy/core/middleware.py` linhas 36-38. | P1 | Em staging/dev fica exposto. | Aplicar rate-limit independente de env; separar limites para login e admin. |
| P1-05 | Admin panel | Rotas `/admin/*` protegidas por `admin_required`, mas sem MFA, sem rate-limit e sem alerta. | `academy/routers/admin.py`, `academy/core/security.py`. | P1 | Credential stuffing/admin takeover. | Adicionar MFA, brute-force lock, logging/alert em admin. |

---

## 5. P2

| ID | Componente | Achado | Evidência | Severidade | Exploração possível? | Correção recomendada |
|----|------------|--------|-----------|-----------|----------------------|----------------------|
| P2-01 | Orchestrator | `git_commit_and_push()` local e executa push para `origin main` sem aprovação humana. | `scripts/orchestrator/orchestrator_central.py` linhas 136-145. | P2 | Publicação/acidente automático em main. | Exigir porta humana ou branch separada; assinar commit. |
| P2-02 | Cron | `cron_email_diario.py` e `cron_whatsapp_diario.py` fazem `subprocess.run` com shell e paths fixos. | `scripts/cron_email_diario.py`, `scripts/cron_whatsapp_diario.py`. | P2 | Injeção via path/nome de arquivo manipulado. | Evitar `shell=True`; sanitizar inputs; rodar em sandbox. |
| P2-03 | Dependências | Sem lockfile confirmado; `requirements.txt` raiz ausente; dependências transitivas não auditadas. | `find` não retornou `requirements.txt` raiz; `academy/requirements.txt` existe. | P2 | Supply chain com versões divergentes/abandonadas. | Congelar dependências; rodar `pip-audit`/`safety`. |
| P2-04 | Logs | `payment_webhook` loga payloads/resultados crus; pode vazar dados sensíveis. | `academy/routers/payments.py` linha 234. | P2 | Dados sensíveis em logs. | Remover/redigir payload de webhook em logs. |
| P2-05 | CI/CD | Actions usam tags não fixadas em `actions/checkout@v4` etc.; não há evidência de approval gate manual antes deploy produção. | `.github/workflows/deploy.yml`, `academy-ci.yml`. | P2 | Comprometimento de action upstream. | Fixar SHA de actions; exigir review manual antes deploy produção. |

---

## 6. P3

| ID | Componente | Achado | Evidência | Severidade | Exploração possível? | Correção recomendada |
|----|------------|--------|-----------|-----------|----------------------|----------------------|
| P3-01 | Segurança | Ausência de MFA em login. | `academy/routers/auth.py`, `academy/core/security.py`. | P3 | Roubo de credencial + acesso admin. | Implementar TOTP/WebAuthn. |
| P3-02 | Backup | Backups locais existem, mas sem política de retenção/restauração testada documentada. | `backup/`, `backups/`, `docs/sales/backups/`. | P3 | Perda em incidente. | Testar restore periodicamente; definir RPO/RTO. |
| P3-03 | Documentação | `.env.example` documenta chave real e valor placeholder idêntico ao código. | `.env.example`. | P3 | Engano operacional. | Padronizar placeholders sem semelhança com produção. |

---

## 7. Informational

- Publication Gate está implementado com bloqueio forte por padrão e múltiplas regras heurísticas.
- Article Generator falha closed quando o gate indisponível (`PublicationGateError`).
- Auth usa JWT com expiração de 7 dias; senha hash bcrypt.
- Content delivery filesystem faz validação de path traversal (`startswith(fs_root)`).
- Logs de request existem, mas não incluem body/credentials.
- Repositório tem branches separadas de deploy (`deploy/pages-safe`), mas main é deploy direto por GitHub Pages.

---

## 8. Unknown

- Configuração real de `APP_ENV=production` e valores reais de `.env` não auditáveis diretamente no momento.
- Segurança do provedor externo real (Hotmart/Mercado Pago/WhatsApp) depende de segredos não verificados.
- Backups de banco não confirmados; restore não testado.

---

## 9. Secrets

Arquivos/segredos identificados:
- `.env`: segredos de SMTP, DB, Hotmart, Mercado Pago, WhatsApp.
- `.env.example`: confirma nomes de segredos e valores placeholder.
- `academy/.env.example`: confirma SECRET_KEY, SMTP, Mercado Pago, WhatsApp.
- `academy/.env.production.example`: confirma variáveis de produção.

Nenhum valor de secret foi exposto aqui.

Recomendação:
- rotacionar segredos suspeitos de exposição;
- remover `.env` do versionamento e usar secrets manager/CI secrets;
- ativar secret scanning no GitHub.

---

## 10. Authentication

Pontos de autenticação:
- `/auth/register`
- `/auth/login`
- `/academy/checkout` usa `get_current_user_optional`
- `/admin/*` usa `admin_required`

Verificações:
- credencial inválida → 401 (BLOCK).
- token expirado/inválido → 401 (BLOCK).
- usuário inexistente → 401 genérico (BLOCK).
- brute-force: apenas via rate-limit em produção; ausente em dev/staging.
- logout/session invalidation: não confirmado nos arquivos auditados.
- MFA: ausente.

---

## 11. Authorization

Papéis mapeados:
- admin
- student
- support

Verificações:
- `/admin/*` checa `admin_required`.
- `/academy/content/*` checa matrícula ativa antes de servir conteúdo.
- `/automation/*` usa `get_current_user`.

Risco:
- endpoints públicos como `/leads` e `/academy/checkout` não exigem autenticação; esperado para captura, mas abre superfície pública.

---

## 12. APIs

Endpoint críticos identificados:
- POST `/academy/checkout`: público; cria matrícula e pagamento.
- GET `/academy/checkout/status`: sem autenticação; retorna status do pedido por `order_id`.
- POST `/academy/payments/webhook`: público; gateway de pagamento.
- GET/POST/PUT/DELETE `/admin/courses`, `/admin/modules`, `/admin/lessons`: admin.
- GET `/admin/leads`, PATCH `/admin/leads/{id}/status`: admin.
- GET `/academy/content/courses/{slug}/filesystem-*`: autenticado + matrícula ativa.
- GET `/monitoring/status`: sem autenticação; expõe integrações/configs.

Riscos:
- `checkout/status` sem auth pode permitir enumeração/rastreamento de pedidos por `order_id`.
- `monitoring/status` sem auth expõe `allowed_origins_count`, variáveis de ambiente e saúde.

---

## 13. Webhooks

Inventariado:
- `POST /academy/payments/webhook`

Evidência:
- Sandbox sempre aceita.
- Hotmart/Mercado Pago/Stripe validam apenas se secret configurado; caso contrário aceitam.
- Sem replay protection explícito.
- Sem idempotência explícita além de `_find_payment`/`_map_status` atualizar status.

Pergunta crítica: se URL conhecida + secret não configurado → forjamento possível. Achado: sim, fora de sandbox.

---

## 14. Database

- ORM: SQLAlchemy.
- DB padrão local: SQLite (`academy.db`) via `DATABASE_URL`.
- Produção espera Postgres pelo `.env.example`.
- Credenciais configuradas por variável de ambiente.
- Migrations/seed scripts existem, mas não foi avaliada segurança da conexão TLS/certificados.

Riscos:
- SQLite local pode ser acessível por path traversal/local attacker.
- Sem confirmação de `sslmode=require` para Postgres.

---

## 15. Academy

- 64 cursos inventariados via `docs/academy/catalog-64-cursos.json` e `inventory-64-cursos.json`.
- Estrutura plana confirmada nos arquivos de catálogo/inventário.
- Routers incluem `proprietarios`, `financeiro`, `content_delivery`, `student`.
- Payment + webhook + checkout + enrollment + certificate estão implementados.
- `content_delivery` restringe arquivos por matrícula ativa e valida path traversal.

---

## 16. Publication Gate

Invariantes observados:
- K3/min_words/min_content_size/min_h2/min_internal_links → BLOCK.
- diversity_ratio < 0.02 → BLOCK (`check_low_specificity`).
- Gate indisponível → `PublicationGateError` → BLOCK.
- `publication_gate_error` → BLOCK em article generator.

Caminhos alternativos:
- direto commit de HTML no `blog/` sem passar pelo gerador/gate; não há bloqueio técnico além de processo/revisão humana.

---

## 17. Article Generator

- `generate_article()` cria arquivo em `blog/`.
- `write_article()` chama `validate_generated_article()` antes de escrever.
- Falha de carga/execução do gate gera `PublicationGateError`.

Pergunta central: existe caminho sem validação?
- sim: publicação manual via commit direto de HTML.

---

## 18. Orchestrator / Agents

- Módulos carregados dinamicamente por path (`importlib.util.spec_from_file_location`).
- `run_*` capturam exceção e retornam dict de erro; não interrompem fluxo.
- `git_commit_and_push()` executa push automático para `origin main`.
- `update_sitemap()` usa `shell=True`.

Risco:
- erro técnico pode ser ignorado e fluxo continua;
- execução remota/local sem assinatura/limite de módulos pode permitir module hijack se attacker controlar paths.

---

## 19. Fail-closed

Pontos observados:
- webhook: bypass quando secret ausente → fail-open.
- orchestrator: exceções genéricas retornam erro JSON, mas chamador pode tratar como sucesso parcial.
- rate limit: desligado fora de produção → fail-open para staging/dev.
- `checkout_confirm` altera matrícula para `active` se pagamento `paid`, sem verificação adicional de fraude/duplicidade.

---

## 20. Logs

- `RequestLoggingMiddleware` registra method/path/status/elapsed.
- `track()` registra eventos em `tracking_events`.
- Pagamento webhook loga resultado e pode expor payload.
- Sem evidência de armazenamento de passwords/tokens explícitos em logs.

Ausências:
- sem log específico de alterações administrativas sensíveis além de tracking genérico;
- sem alerta por log.

---

## 21. Monitoramento

Verificado:
- `/monitoring/status` existe e mostra DB/courses/enrollments/payments.

Ausente/desconhecido:
- alertas para múltiplos logins falhos;
- alertas para `PublicationGateError`;
- alertas para falha de cron/orquestrador;
- alertas para alterações administrativas;
- alertas para webhook rejeitado/forjado.

---

## 22. Backups

- Backups locais existem em `backup/`, `backups/`, `docs/sales/backups/`, `litoral-prime-imoveis/backups/`.
- Sem política explícita de retenção, criptografia ou restore testado documentado.

Status: BACKUP EXISTE | RESTORE NÃO TESTADO | RETENÇÃO NÃO CONFIRMADA

---

## 23. CI/CD

- Deploy GitHub Pages em push para `main`.
- `academy-ci.yml` executa testes + validação de inventário.
- Falta:
  - proteção de branch obrigatória antes deploy produção;
  - secret scanning;
  - SBOM/dependency review;
  - bloqueio manual/approval para deploy produção.

---

## 24. Supply chain

- Actions sem pin de SHA.
- Sem lockfile de Python confirmado na raiz.
- Backend serverless em `backend/` usa funções Vercel/Netlify sem dependências de produção auditadas no baseline.

---

## 25. Recomendações priorizadas

1. Remover `.env` do repo e migrar segredos para vault/CI secrets + secret scanning.
2. Tornar `verify_webhook` fail-closed quando segredo ausente; bloquear evento.
3. Restringir CORS para domínios autorizados e desativar `allow_credentials=True` com `*`.
4. Aplicar rate-limit e brute-force protection em login/admin independente de ambiente.
5. Exigir aprovação humana antes deploy produção e fixar SHAs de actions.
6. Adicionar MFA e logging/alertas em admin.
7. Testar restore de backup e definir RPO/RTO.
8. Auditar dependências com lockfile e scanner de vulnerabilidades.

---

## 26. Matriz de risco

| ID | Componente | Achado | Evidência | Severidade | Exploração possível? | Correção recomendada |
|----|------------|--------|-----------|-----------|----------------------|----------------------|
| SEC-01 | Secrets | `.env` com segredos presente; commit acidental pode expor SMTP/Hotmart/Mercado Pago/WhatsApp/DB. | `.env.example`; `.env` existe na raiz. | P1 | Sim | Remover do versionamento; usar secrets manager; secret scanning. |
| SEC-02 | Webhook | `verify_webhook` aceita eventos quando secret/config ausente. | `academy/core/payments/webhooks.py` | P1 | Sim | Fail-closed quando segredo ausente; bloquear e logar. |
| SEC-03 | API/CORS | CORS aberto por padrão com credenciais. | `academy/main.py` | P1 | Sim | Restringir origins por env. |
| SEC-04 | Auth | Rate limit só em produção; ausência de MFA/2FA. | `academy/core/middleware.py` | P1 | Sim | Rate limit global; adicionar MFA. |
| SEC-05 | Admin | Sem brute-force lock/alertas. | `academy/core/security.py`, `academy/routers/admin.py` | P1 | Sim | Lockout, MFA, alerta. |
| SEC-06 | Orchestrator | Push automático para main sem porta humana. | `scripts/orchestrator/orchestrator_central.py` | P2 | Possível | Exigir branch/review para deploy. |
| SEC-07 | Cron | `subprocess.run(..., shell=True)` com paths fixos. | `scripts/cron_*.py` | P2 | Possível | Remover shell=True; sanitizar paths. |
| SEC-08 | Supply chain | Actions sem pin; dependências sem lockfile confirmado. | `.github/workflows/*.yml` | P2 | Possível | Fixar SHAs; lockfile + audit. |
| SEC-09 | Logs | Webhook loga payload cru. | `academy/routers/payments.py` | P2 | Possível | Redigir payload em log. |
| SEC-10 | Publication Gate | Não há bloqueio técnico contra commit manual de HTML sem gate. | `blog/` commit manual possível | P2 | Possível | Pre-commit hook + CI gate. |

---

## 27. Security Invariants

Proposta de invariantes automatizáveis:

- unauthorized request → BLOCK
- invalid token → BLOCK
- expired token → BLOCK
- invalid webhook → BLOCK
- webhook without configured secret → BLOCK
- publication without validation → BLOCK
- admin action without MFA/authorized session → BLOCK
- CORS wildcard with credentials in production → BLOCK
- secret missing in production → FAIL-CLOSED
- permission missing → BLOCK
- orchestrator deploy without human gate → BLOCK
- shell-injectable cron path → BLOCK
- monitoring status without auth → BLOCK
- checkout status without minimal auth/trace → BLOCK

---

## 28. Evidência

Arquivos-chave auditados:
- `academy/core/auth.py`
- `academy/core/security.py`
- `academy/core/middleware.py`
- `academy/core/config.py`
- `academy/core/database.py`
- `academy/core/models.py`
- `academy/core/payments/webhooks.py`
- `academy/main.py`
- `academy/routers/admin.py`
- `academy/routers/admin_content.py`
- `academy/routers/admin_leads.py`
- `academy/routers/auth.py`
- `academy/routers/leads.py`
- `academy/routers/payments.py`
- `academy/routers/content_delivery.py`
- `academy/routers/monitoring.py`
- `scripts/orchestrator/modules/publication_gate.py`
- `scripts/orchestrator/modules/article_generator.py`
- `scripts/orchestrator/orchestrator_central.py`
- `scripts/cron_email_diario.py`
- `scripts/cron_whatsapp_diario.py`
- `.github/workflows/deploy.yml`
- `.github/workflows/academy-ci.yml`
- `.env.example`
- `academy/.env.example`
- `academy/.env.production.example`

Nenhuma exploração destrutiva foi realizada. Nenhum segredo foi exposto integralmente.

---

## 29. Plano de correção priorizado

Fase 1 — Imediata:
1. Revogar/rotacionar segredos suspeitos e remover `.env` do versionamento.
2. Implementar fail-closed em `verify_webhook()`.
3. Restringir CORS em produção.

Fase 2 — Curto prazo:
4. Aplicar rate-limit global e brute-force protection.
5. Adicionar MFA para admin.
6. Fixar SHAs de GitHub Actions e adicionar approval manual para deploy produção.
7. Redigir payload de webhook em logs.

Fase 3 — Médio prazo:
8. Testar restore de backups; documentar RPO/RTO.
9. Auditar e fixar dependências com lockfile + scanner.
10. Implementar pre-commit hook/CI gate contra bypass do Publication Gate.
11. Revisar orquestrador/cron para princípio do menor privilégio.

---

FIM DO RELATÓRIO
