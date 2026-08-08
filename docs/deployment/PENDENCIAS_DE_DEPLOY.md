# PENDÊNCIAS DE DEPLOY — Academy Praia Digital

Esta lista contém **apenas** itens que dependem do Render ou de serviços externos.

## Autenticação no Render
- Login no Render dashboard OU fornecimento de API key do Render.

## Provisionamento no Render
- Criação do Web Service `praia-digital-academy`.
- Criação do PostgreSQL `academy-db`.
- Configuração de variáveis de ambiente no Render (`SECRET_KEY`, `DATABASE_URL`, `SMTP_*`, `ALLOWED_ORIGINS`, etc.).
- Deploy automático via `render.yaml`.

## DNS e Domínio
- Configuração de domínio customizado `academy.praia.digital` no Render.
- Propagação DNS.
- Validação pós-deploy com `scripts/validate_academy_deploy.py`.

## Serviços externos (integrações)
- **E-mail:** configuração de SMTP real para envio de confirmações e instruções.
- **Pagamento:** credenciais do gateway de pagamento para checkout real.
- **WhatsApp:** tokens e número para atendimento automático.
- **CDN/hospedagem de arquivos:** para entrega de PDFs e materiais digitais em produção.

## Quando destravar
Assim que o Render estiver acessível, executar:
1. `python scripts/validate_academy_deploy.py`
2. Verificar health, HTTPS, headers, `/docs`, `/auth/register`, `/leads`, `/monitoring/status`.
3. Corrigir eventuais erros de produção.
4. Confirmir `academy.praia.digital` acessível.
