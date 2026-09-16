# Contribuindo com a Praia Digital

Obrigado por contribuir! Este repositório é principalmente um site estático com scripts Python de apoio.

## Fluxo de trabalho

1. Crie uma branch a partir de `main`: `feat/nome-curto` ou `fix/nome-curto`.
2. Faça commits pequenos com mensagens no estilo Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`).
3. Abra um Pull Request preenchendo o template.

## ⚠️ Automações concorrentes

Este repo recebe sincronizações/rebases automáticos do upstream (`acarolmourad-commits/praia-digital`). Rebase/force-push em `main` pode apagar commits recentes. Antes de rodar automações que reescrevem histórico, verifique se há commits novos em `main` (compare com o último commit listado em `git log`).

## Regras de conteúdo

- Idioma: português (pt-BR).
- Domínio canônico: sempre `https://praia.digital` em canonicals, Open Graph e redirects.
- Páginas novas precisam de `<title>`, meta description, canonical e heading único (`<h1>`).
- Não duplique páginas: consolide variações com redirect (ver `politica-privacidade.html` como exemplo).

## Qualidade antes do PR

```bash
python check_links.py   # links quebrados
```

## Segurança

- Nunca commite credenciais; use `.env` (modelo em `.env.example`).
- O CI executa varredura de segredos — PRs com segredos serão bloqueados.
- Vulnerabilidades: reporte de forma privada conforme `security.txt`.
