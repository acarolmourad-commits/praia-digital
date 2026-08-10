# Checklist Pós-Deploy — Academy no Render

Execute após criar/configurar o Web Service e apontar o DNS.

## 1) Verificações de saúde
- [ ] `GET https://academy.praia.digital/health` retorna `{"status":"ok","service":"academy-api"}`
- [ ] `GET https://academy.praia.digital/docs` retorna `200`

## 2) Banco e dados iniciais
- [ ] `GET https://academy.praia.digital/monitoring/status` retorna `200`
- [ ] `"database":"ok"` presente no JSON

## 3) Autenticação pública
- [ ] `POST https://academy.praia.digital/auth/register` com payload válido retorna `200`
- [ ] `POST https://academy.praia.digital/auth/login` retorna token Bearer válido

## 4) Checkout público
- [ ] `POST https://academy.praia.digital/payments/checkout` retorna `200`
- [ ] Response contém `"status":"pending"` ou URL de checkout

## 5) Frontend Academy
- [ ] `GET https://academy.praia.digital/education/index.html` -> `200`
- [ ] `GET https://academy.praia.digital/education/cursos/index.html` -> `200`
- [ ] `GET https://academy.praia.digital/education/aluno/login.html` -> `200`
- [ ] `GET https://academy.praia.digital/education/aluno/index.html` -> `200`
- [ ] `GET https://academy.praia.digital/education/aluno/curso.html` -> `200`
- [ ] `GET https://academy.praia.digital/education/aluno/progresso.html` -> `200`
- [ ] `GET https://academy.praia.digital/education/aluno/certificado.html` -> `200`
- [ ] `GET https://academy.praia.digital/education/aluno/admin.html` -> `200`
- [ ] `GET https://academy.praia.digital/education/vendas.html` -> `200`

## 6) CORS / domínio
- [ ] `OPTIONS` raiz/frontends não retornam erro de origem bloqueada
- [ ] `academy.praia.digital` não redireciona para URL do Render (`*.onrender.com`)

## 7) Integrações (modo stub permitido em Fase 1)
- [ ] `/leads` aceita POST e retorna `200`
- [ ] `/automation/whatsapp-notify/{enrollment_id}` retorna `200` ou `404` controlado
- [ ] `/automation/email-confirmation/{enrollment_id}` retorna `200` ou `404` controlado

## 8) Frontend principal
- [ ] `https://praia.digital` segue OK
- [ ] Rotas públicas principais retornam `200`
