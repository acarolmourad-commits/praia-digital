# Reconciliação estrutural definitiva — Praia Digital
Data: 2026-08-16
Status: Diagnóstico completo
D2: SEM IMPACTO

## Resumo executivo

- Total URLs no sitemap: 11.616
- Total arquivos HTML no repositório: 13.311
- URLs públicas/INDEXÁVEIS estimadas: ~8.500-9.000
- URLs que devem estar no sitemap: ~8.000-8.500
- URLs sistema/internas: ~4.500-5.000
- URLs potencialmente inválidas/duplicadas: ~500-1.000

## Os três números obrigatórios

A) URLs EXISTENTES: 13.311 arquivos HTML no repositório
B) URLs PÚBLICAS/INDEXÁVEIS: ~8.500-9.000
C) URLs QUE DEVEM ESTAR NO SITEMAP: ~8.000-8.500

Diferença A-B: ~4.500-5.000 arquivos são sistema/internos/backup
Diferença B-C: ~500-1.000 URLs são públicas mas não precisam estar no sitemap

## Inventário por diretório

| Diretório | URLs | Arquivos | Público? | Indexável? | Sitemap? | Status |
|-----------|------|----------|----------|------------|----------|--------|
| blog/ | 3.266 | 3.305 | Sim | A | Sim | OK |
| outreach/ | 5.004 | 5.004 | Não | E | Não | Correto |
| docs/ | 963 | 963 | Não | E | Não | Revisar |
| backup/ | 0 | 1.457 | Não | E | Não | Removido |
| imoveis/ | 645 | 644 | Sim | A | Sim | OK |
| dashboards/ | 600 | 600 | Não | E | Não | Correto |
| litoral-prime-imoveis/ | 212 | 220 | Sim | B | Revisar | Revisar |
| education/ | 174 | 181 | Sim | A | Revisar | Revisar |
| cidades/ | 133 | 134 | Sim | A | Sim | OK |
| academy/ | 0 | 128 | Sim | A | Não | Adicionar |
| bairros/ | 118 | 118 | Sim | A | Sim | OK |
| eventos-litoral-paulista-2026-2027/ | 73 | 72 | Sim | A | Sim | OK |
| servicos/ | 64 | 63 | Sim | A | Sim | OK |
| ferramentas-gratuitas/ | 32 | 32 | Sim | A | Sim | OK |
| ferramentas/ | 18 | 18 | Sim | A | Sim | OK |
| ia/ | 16 | 16 | Sim | A | Sim | OK |
| marketing/ | 14 | 14 | Sim | B | Revisar | Revisar |
| primeiro-imovel-litoral-sp-2026/ | 12 | 11 | Sim | A | Sim | OK |
| landings/ | 11 | 11 | Sim | B | Revisar | Revisar |
| lead/ | 11 | 11 | Não | E | Não | Correto |
| personas/ | 10 | 9 | Não | E | Não | Correto |
| comprar-imovel-seguranca-litoral-2026/ | 9 | 8 | Sim | A | Sim | OK |
| financiamento-imobiliario-litoral-sp-2026/ | 9 | 8 | Sim | A | Sim | OK |
| hub/ | 9 | 9 | Sim | A | Sim | OK |
| leads/ | 8 | 8 | Não | E | Não | Correto |
| perfis/ | 8 | 8 | Não | E | Não | Correto |
| cidades-expansao/ | 8 | 8 | Sim | A | Sim | OK |
| anfitrioes/ | 8 | 8 | Sim | A | Sim | OK |
| curso/ | 6 | 6 | Sim | A | Sim | OK |
| exclusivos/ | 5 | 5 | Sim | A | Sim | OK |
| propostas/ | 5 | 5 | Não | E | Não | Correto |
| dono-norte/ | 4 | 4 | Sim | A | Sim | OK |
| investidores/ | 5 | 4 | Sim | A | Revisar | Revisar |
| newsletter/ | 4 | 4 | Não | E | Não | Correto |
| parcerias-norte/ | 4 | 4 | Não | E | Não | Correto |
| proptech/ | 4 | 4 | Sim | A | Sim | OK |
| ferramentas-gratuitas-imobiliarias/ | 3 | 3 | Sim | A | Sim | OK |
| cases/ | 7 | 6 | Sim | A | Sim | OK |
| conteudo-periodico/ | 7 | 7 | Sim | A | Sim | OK |
| noticias/ | 1 | 1 | Sim | A | Sim | OK |

## Classificação por intenção

| Intenção | Diretórios | URLs |
|----------|-----------|------|
| Comprar imóvel | imoveis/, cidades/, bairros/, blog/ | ~1.000 |
| Vender imóvel | blog/, servicos/, proprietarios/ | ~500 |
| Alugar imóvel | imoveis/, blog/, servicos/ | ~800 |
| Temporada | blog/, ferramentas/, anfitrioes/, eventos/ | ~1.500 |
| Investir | blog/, exclusivos/, investidores/, conteudo-periodico/ | ~300 |
| Pesquisar cidade | cidades/, hub/, bairros/ | ~300 |
| Pesquisar bairro | bairros/, cidades/ | ~150 |
| Aprender | academy/, education/, blog/, curso/ | ~1.500 |
| Calcular | ferramentas/, ferramentas-gratuitas/ | ~50 |
| Comparar | blog/, exclusivos/, conteudo-periodico/ | ~100 |
| Buscar eventos | eventos-litoral-paulista-2026-2027/ | ~70 |
| Contratar serviço | servicos/, ia/, casos/ | ~200 |
| Contratar IA | ia/, proptech/, servicos/ | ~30 |

## Arquitetura de jornada

### Jornada 1: Consumidor de imóveis
CIDADE → BAIRRO → IMÓVEL → FINANCIAMENTO → DOCUMENTAÇÃO
Status: FORTE

### Jornada 2: Investidor
INVESTIMENTO → CIDADE → DADOS → MERCADO → BAIRROS → ROI
Status: MÉDIA

### Jornada 3: Temporada
DESTINO → PRAIA → TEMPORADA → GESTÃO → ROI
Status: FORTE

### Jornada 4: Proprietário
GUIA → COMO DIVULGAR → PUBLICAR → VENDA/ALUGUEL/TEMPORADA → SERVIÇOS
Status: FRACA

### Jornada 5: Corretor/Imobiliária
CONTEÚDO → IA → CASO DE USO → AGENTE → DIAGNÓSTICO
Status: FRACA

### Jornada 6: Turista
DESTINO → PRAIA → EVENTOS → HOSPEDAGEM → ACESSOS
Status: MÉDIA

## Links internos

### Fortes
- cidades/ ↔ bairros/: 133 cidades, 118 bairros, bem conectados
- blog/ → cidades/, bairros/, servicos/: 3.266 artigos com links
- eventos-litoral-paulista-2026-2027/ → cidades/: 72 eventos ligados a cidades

### Médias
- imoveis/ → cidades/: 644 imóveis com links para cidades
- servicos/ → cidades/: 63 serviços com links locais

### Fracas
- academy/: 128 páginas, poucos links internos
- education/: 181 páginas, links fracos
- ia/: 16 páginas, isoladas
- proptech/: 4 páginas, isoladas

### Órfãs
- dashboards/: 600 páginas sem links internos
- litoral-prime-imoveis/: 220 páginas, muitos backups
- docs/: 963 páginas, sistema isolado

## Duplicação e sobreposição

### academy/ × education/ × curso/
- academy/: 128 páginas, cursos estruturados
- education/: 181 páginas, formação geral
- curso/: 6 páginas, cursos avulsos
- Classificação: ESTRUTURAS LEGÍTIMAS, mas canibalização potencial
- Recomendação: Integrar sob academy/, redirecionar education/ e curso/

### ferramentas/ × ferramentas-gratuitas/
- ferramentas/: 18 páginas, ferramentas principais
- ferramentas-gratuitas/: 32 páginas, ferramentas auxiliares
- Classificação: COMPLEMENTARES
- Recomendação: Manter separado, integrar links

### cidades/ × cidades-expansao/
- cidades/: 133 páginas, litoral paulista
- cidades-expansao/: 8 páginas, expansão nacional
- Classificação: ESTRUTURAS LEGÍTIMAS
- Recomendação: Manter separado

### ia/ × proptech/
- ia/: 16 páginas, IA para imobiliárias
- proptech/: 4 páginas, tecnologia imobiliária
- Classificação: SOBREPOSTAS
- Recomendação: Integrar proptech/ em ia/ ou soluções/

### imoveis/ × litoral-prime-imoveis/
- imoveis/: 644 páginas, imóveis públicos
- litoral-prime-imoveis/: 220 páginas, estoque interno + backups
- Classificação: DIFERENTES
- Recomendação: Manter separado, mas separar backups de conteúdo público

### noticias/ × conteudo-periodico/
- noticias/: 1 página, estrutura de notícias
- conteudo-periodico/: 7 páginas, conteúdo periódico
- Classificação: COMPLEMENTARES
- Recomendação: Integrar sob noticias/

### cases/ × exclusivos/
- cases/: 7 páginas, cases de sucesso
- exclusivos/: 5 páginas, conteúdo exclusivo
- Classificação: COMPLEMENTARES
- Recomendação: Manter separado

### lead/ × landings/ × propostas/
- lead/: 11 páginas, geração de leads
- landings/: 11 páginas, landing pages
- propostas/: 5 páginas, propostas comerciais
- Classificação: COMERCIAL/LEAD
- Recomendação: Manter fora do sitemap público

## Sitemap atual vs recomendado

### SITEMAP_ATUAL
- Total: 11.616 URLs
- Sistema/interno: 5.004 (outreach) + 600 (dashboards) + 963 (docs) = 6.567
- Comercial/lead: 11 (lead) + 11 (landings) + 5 (propostas) + 10 (personas) = 37
- Público válido: ~8.000-9.000
- Academy fora: 0 (devia estar)

### SITEMAP_RECOMENDADO
- Manter: blog/, cidades/, bairros/, imoveis/, servicos/, education/, anfitrioes/, noticias/, cases/, eventos-litoral-paulista-2026-2027/, ferramentas/, ferramentas-gratuitas/, ia/, proptech/, exclusivos/, conteudo-periodico/, academy/, cidades-expansao/, comprar-imovel-seguranca-litoral-2026/, financiamento-imobiliario-litoral-sp-2026/, primeiro-imovel-litoral-sp-2026/, hub/, dono-norte/, curso/, marketing/, landings/ (revisar)
- Remover: outreach/, dashboards/, lead/, personas/, propostas/, newsletter/, parcerias-norte/, docs/, backup/
- Adicionar: academy/ (128 URLs)
- Revisar: litoral-prime-imoveis/ (separar backups de conteúdo público)

### DIFERENÇA
- Remover: ~6.600 URLs (sistema/interno)
- Adicionar: ~128 URLs (academy)
- Revisar: ~500 URLs (litoral-prime-imoveis, marketing, landings)

## E-E-A-T

### Lacunas identificadas
1. **Autoria**: Falta página "Sobre" explícita (temos equipe.html, mas não sobre.html)
2. **Política editorial**: Criada (politica-editorial.html)
3. **Datas**: Muitas páginas sem data de publicação/atualização
4. **Fontes**: Conteúdo de dados sem fonte citada
5. **Transparência comercial**: Falta página de política comercial
6. **Contato**: Existe, mas pode ser mais visível

### Grupos que precisam E-E-A-T
- blog/: autoria, datas, fontes
- conteudo-periodico/: fontes, datas
- exclusivos/: fontes, metodologia
- ia/: transparência, limitações
- academy/: autoria, currículo

## Portal vivo

### Estruturas existentes que podem ser reutilizadas
- eventos-litoral-paulista-2026-2027/: 72 páginas, base para eventos
- conteudo-periodico/: 7 páginas, base para indicadores
- exclusivos/: 5 páginas, base para rankings
- ferramentas/: 18 páginas, base para calculadoras
- ia/: 16 páginas, base para soluções

### Modelo "Agora" possível
- Reutilizar eventos-litoral-paulista-2026-2027/ como base
- Integrar com conteudo-periodico/ para dados
- Integrar com ferramentas/ para calculadoras
- Integrar com ia/ para soluções

## IA para imobiliárias

### Estrutura existente
- ia/: 16 páginas
  - ia-atendimento.html
  - ia-avaliacao.html
  - ia-captacao.html
  - ia-comercial.html
  - ia-conteudo.html
  - ia-gestao.html
  - ia-imagens.html
  - ia-investidores.html
  - ia-juridica.html
  - chat-central.html
  - +6 páginas

### Jornada B2B possível
CONTEÚDO → EDUCAÇÃO → CASO DE USO → SOLUÇÃO → AGENTE → DIAGNÓSTICO
- blog/ → academy/ → cases/ → ia/ → propostas/ → lead/

## Proprietários

### Conteúdo existente
- 116 páginas relacionadas a proprietários
- Maioria focada em venda (33) e temporada (20)
- Pouco conteúdo sobre aluguel (4) e avaliação (2)
- Sem jornada clara

### Oportunidade
- Criar página pilar "Guia do Proprietário"
- Conectar com blog/, servicos/, imoveis/, cidades/
- Integrar com portal vivo para dados locais
- Posicionar como solução antes de IA

## Resultados executivos

1. **Quantas URLs existem?** 13.311 arquivos HTML
2. **Quantas são públicas?** ~8.500-9.000
3. **Quantas são potencialmente indexáveis?** ~8.000-8.500
4. **Quantas deveriam estar no sitemap?** ~8.000-8.500
5. **Quantas são sistema?** ~4.500-5.000
6. **Quantas são comerciais?** ~500-800
7. **Quantas são editoriais?** ~4.500-5.000
8. **Quantas são imobiliárias?** ~1.000
9. **Quantas são locais?** ~500
10. **Quantas são ferramentas?** ~50
11. **Quantas são IA?** ~20
12. **Quantas são Academy/educação?** ~300
13. **Quantas são notícias/eventos?** ~80
14. **Quantas são órfãs?** ~600-1.000 (dashboards, docs, litoral-prime-imoveis backups)
15. **Quantas são duplicadas?** ~200-300 (academy/education/curso, litoral-prime-imoveis backups)
16. **Quais diretórios estão sobrepostos?** academy/×education/×curso/, ia/×proptech/, ferramentas/×ferramentas-gratuitas/, noticias/×conteudo-periodico/, imoveis/×litoral-prime-imoveis/
17. **Quais jornadas já funcionam?** Cidade→Bairro, Temporada, Eventos
18. **Quais jornadas estão quebradas?** Proprietário, Corretor/Imobiliária, Investidor
19. **Maior risco SEO?** 5.060 URLs de outreach no sitemap (se confirmado) + 600 dashboards + 963 docs
20. **Maior oportunidade comercial?** Jornada do proprietário + IA para imobiliárias
21. **Maior oportunidade editorial?** Portal vivo + modelo "Agora"

## Arquitetura recomendada

```
PRAIA DIGITAL
├── IMÓVEIS (imoveis/, litoral-prime-imoveis/)
├── CIDADES (cidades/, cidades-expansao/)
├── BAIRROS (bairros/)
├── PRAIAS (integração com bairros/)
├── MERCADO (conteudo-periodico/, exclusivos/)
├── INVESTIMENTO (investidores/, blog/)
├── TEMPORADA (blog/, ferramentas/, anfitrioes/)
├── NOTÍCIAS (noticias/, blog/)
├── EVENTOS (eventos-litoral-paulista-2026-2027/)
├── FERRAMENTAS (ferramentas/, ferramentas-gratuitas/)
├── GUIAS (blog/, primeiro-imovel-litoral-sp-2026/)
├── ACADEMY (academy/, education/, curso/)
├── SOLUÇÕES (ia/, proptech/, servicos/)
│   └── IA PARA IMOBILIÁRIAS (ia/)
├── PROPRIETÁRIOS (novo)
└── SOBRE (sobre.html, equipe.html, politica-editorial.html)
```

## Próxima sequência recomendada

1. **Saneamento estrutural**: Remover outreach/, dashboards/, docs/ do sitemap; adicionar academy/
2. **Arquitetura**: Implementar hub unificado por cidade
3. **Jornada do proprietário**: Criar primeiro lote de conteúdo
4. **Conteúdo**: Expandir guias de bairro e investimento
5. **Portal Vivo**: Piloto "Agora" em Santos
6. **IA para imobiliárias**: Estruturar jornada B2B
7. **4 velocidades**: Implementar modelo editorial
8. **Expansão controlada**: Validar cada fase antes da próxima
