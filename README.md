# Praia Digital

Tecnologia especializada no mercado imobiliário do litoral brasileiro. Catálogo de imóveis, conteúdo SEO local, ferramentas gratuitas para imobiliárias/corretores e automações de captação e follow-up de leads.

**Site:** https://praia.digital

## Visão geral

Site estático (HTML/CSS/JS) com páginas de conteúdo otimizadas para SEO local (Baixada Santista e Litoral Norte de SP), landing pages de captação, calculadoras, propostas comerciais e scripts de automação em Python.

## Estrutura do repositório

| Caminho | Descrição |
|---|---|
| `index.html` | Página inicial |
| `imoveis.html`, `mapa-inteligente.html` | Catálogo e busca de imóveis |
| `*.html` (raiz) | Páginas de conteúdo SEO, FAQs, landings e propostas |
| `bairros/`, `cidades/`, `imoveis/`, `blog/`, `noticias/` | Conteúdo organizado por seção |
| `academy/`, `curso/`, `education/` | Cursos e trilhas educacionais |
| `api/`, `backend/`, `automation/` | Backend e automações |
| `scripts/`, `check_links.py`, `audit_imoveis.py` | Scripts de manutenção e auditoria |
| `feed.xml`, `sitemap.xml`, `llms.txt`, `llms-full.txt` | SEO e descoberta por LLMs |
| `netlify.toml`, `vercel.json`, `render.yaml`, `Dockerfile`, `railway.json` | Configs de deploy |

## Deploy

O site é estático e pode ser publicado via Netlify (`netlify.toml`), Vercel (`vercel.json`), Render (`render.yaml`) ou Docker (`Dockerfile`). O domínio canônico é `praia.digital` (ver `CNAME` e `_redirects`).

## CI / Qualidade

Workflows em `.github/workflows/`:

- `deploy.yml` / `deploy-indexnow.yml` — deploy e submissão IndexNow
- `secret-scan.yml` — varredura de segredos (baseline em `.secrets.baseline`)
- `academy-ci.yml` — CI da área Academy
- `content-evolution.yml`, `nav-simplification.yml` — automações de conteúdo
- `link-check.yml` — auditoria semanal de links quebrados (`check_links.py`)

O Dependabot mantém GitHub Actions e dependências Python atualizados.

## Scripts úteis

```bash
python check_links.py      # audita links internos/externos; gera link_check_report.json
python audit_imoveis.py    # audita páginas de imóveis; gera relatorio_auditoria_imoveis.json
```

## Integrações e automação

As automações de follow-up (WhatsApp, e-mail, CRM) seguem as práticas descritas em [`docs/COMPOSIO-INTEGRACAO.md`](docs/COMPOSIO-INTEGRACAO.md).

## Contribuindo

Leia [`CONTRIBUTING.md`](CONTRIBUTING.md). Reporte bugs e sugira features usando os templates de issue.

## Licença

[MIT](LICENSE)
