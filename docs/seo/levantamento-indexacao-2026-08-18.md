# Levantamento técnico — indexação
Data: 2026-08-18
Status: Diagnóstico factual, sem correções

## 1. Fontes utilizadas
- `sitemap.xml` — 11.880 URLs
- `robots.txt`
- `docs/seo/gsc-improvement-plan-2026-08-17.md`
- `docs/seo/gsc-improvement-checklist-pos-d2-2026-08-17.md`
- `docs/seo/technical_audit_2026-08-16.md`
- `docs/seo/full_audit_2026-08-16.json`
- Varredura local de `meta robots`, `canonical`, `noindex`
- Inventário local de HTML por diretório

## 2. Limitações
- Nenhum export oficial do Google Search Console com lista de URLs "não indexadas" foi encontrado no projeto.
- Os dados de GSC existentes (`2026-08-17`) mostram **posições e impressões**, não erros de indexação.
- Sem acesso a `URL Inspection` ou `Index Coverage` exportado, não é possível confirmar categoria A diretamente.

## 3. Total analisado
- Sitemap: 11.880 URLs
- HTML no repositório: 4.828
- Páginas com `noindex` detectadas: 12

## 4. URLs com evidência de não indexação
Nenhuma. Nenhuma fonte no projeto declara explicitamente URLs como "não indexadas pelo Google".

## 5. URLs potencialmente não indexadas
Nenhuma suspeita técnica forte encontrada. Todos os `noindex` detectados são intencionais:
- `404.html` — correto
- `education/checkout.html` — transactional, correto
- `education/aluno/*` (7 páginas) — área de aluno, correto
- `servicos/template-cidade-servico.html` — template, correto
- `servicos/midia-profissional.html` — redirect page, correto
- `litoral-prime-imoveis/servicos/template-cidade-servico.html` — template, correto

## 6. URLs sem problema técnico aparente
Todas as páginas públicas de conteúdo, serviços, blog, cidades, bairros, education, anfitriões e docs:
- Possuem `canonical` próprio na maior parte das amostras verificadas
- Não possuem `noindex`
- Não são bloqueadas por `robots.txt`
- Estão no `sitemap.xml`
- Respondem HTTP 200 localmente

## 7. Causas prováveis
- **Nenhuma causa técnica de não indexação confirmada no projeto.**
- Os dados de GSC existentes mostram que o site está ranqueando para queries relevantes (`investir imóveis litoral paulista`, `ia para imobiliarias`, `sauna em são vicente`, etc.), o que indica indexação ativa.
- Diferença entre o número esperado (~20) e o número encontrado (0): provavelmente o dado de ~20 páginas não indexadas veio de uma fonte externa não presente no repositório.

## 8. Nível de confiança
- **Alta confiança** para: "não há evidência local de problema de indexação em massa".
- **Não confirmável localmente**: lista oficial de URLs não indexadas no Google.

## 9. Prioridades
- P1: Aguardar export oficial do GSC (`Index Coverage` / `URL Inspection`) para confirmar/negar as ~20 URLs.
- P2: Remover 1.475 URLs de `/backup/` do `sitemap.xml` (se confirmado que não devem ser indexadas).
- P3: Monitorar `robots.txt` para bloquear `/backup/` se necessário.

## 10. Dados ainda necessários do Google Search Console
- Relatório de **Cobertura do índice** (`Index Coverage`)
- Lista de URLs com status **"Rastreada, não indexada"** ou **"Erro de indexação"**
- Export de **URL Inspection** para as supostas ~20 páginas
- Relatório de **Sitemaps** — validar se há warnings/erros

## Conclusão
Com as fontes disponíveis no projeto, **não é possível confirmar a existência de 20 páginas não indexadas**. O diagnóstico técnico local indica que o site está estruturalmente indexável. Próximo passo obrigatório: obter dados diretos do GSC.
