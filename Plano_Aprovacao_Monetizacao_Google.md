# Plano de Aprovação na Monetização do Google — Praia Digital

**Data:** 31/08/2026  
**Site:** https://praia.digital  
**Documento de referência:** https://docs.google.com/document/d/1RvW579_ezqntEjLG2TrhMz2SYRm0rCdFa1dhT-FGpD0/edit

---

## 1. Diagnóstico atual de conformidade

### Páginas obrigatórias
- Presentes: Política de Privacidade, Sobre, Contato, FAQ.
- Ausentes: Termos de Uso, Quem Somos, Fale Conosco.
- Página Sobre expandida hoje para ~480 palavras e pilares E-E-A-T.

### Conteúdo e UX
- Home com conteúdo denso; blog com hub, mas ainda sem profundidade suficiente em artigos principais.
- Nenhum link quebrado na amostra auditada.
- Navegação preservada; páginas canônicas e meta description ok.

### Técnico / Search Console
- `sitemap.xml`: 12.044 URLs, tamanho 2,6MB — enviado e acessível.
- `robots.txt`: permite indexação geral.
- `ads.txt`: linha exata do publisher `google.com, pub-9562601722232986, DIRECT, f08c47fec0942fa0`.
- **Search Console:** página inicial detectada; ainda não confirmada propriedade verificada de `praia.digital` no painel. É necessário concluir a verificação de propriedade antes de ler relatórios.

### E-mail e alertas
- Gmail Web aberto: conta `comercial@praia.digital`.
- Busca automatizada não aplicável por limitações do browser helper; não há bloqueios aparentes, mas não foi possível enumerar alertas nesta rodada.

### Composio / Instagram / Gmail
- Instagram: conexão ACTIVE (`praia_digital`), 1 conversa mapeada.
- Gmail/Composio: autenticação pendente — aguardando conclusão manual no link enviado.
- Google Workspace local: indisponível para escrita automatizada agora; browser será usado como fallback.

---

## 2. Correções prioritárias

1. Concluir autenticação do Composio no Gmail.
2. Verificar propriedade do Search Console e revisar Cobertura/Indexação.
3. Revisar política de conteúdo: transformar artigos genéricos em guias específicos por cidade/bairro.
4. Adicionar “Quem Somos” e “Fale Conosco” com conteúdo original.
5. Confirmar snippets AdSense corretos no head da home e páginas-chave.

---

## 3. Cronograma estimado — 7 dias

- D1: Concluir conexões (Gmail ACTIVE + Search Console acessível).
- D2: Corrigir conteúdo fino/generico em 3–5 artigos.
- D3: Publicar /quem-somos e /fale-conosco.
- D4: Checar indexação e erros no Search Console.
- D5: Revisar snippets AdSense e meta tags em páginas-chave.
- D6: Auditoria final de UX e links internos.
- D7: Submissão/reesubmissão da monetização quando checklist estiver verde.

---

## 4. Próximos passos operacionais

- Validar Gmail ACTIVE: abra `https://connect.composio.dev/link/lk_Q6EIIDCo54mY`.
- No Search Console, abra a propriedade `praia.digital` e confirme: “Sitemaps” + “Cobertura”.
- Responder aqui e eu continuo automaticamente na importação dos contatos para Sheets e na verificação dos alertas.

---

## 5. Progresso — 15/09/2026

### Concluído (nesta rodada)
- ✅ **Item 4:** páginas `quem-somos.html` e `fale-conosco.html` criadas com conteúdo original, schema.org (`AboutPage`/`ContactPage`), canonical e OG tags. Commits no fork `praiadigital/praia-digital`.
- ✅ **Item 5 (parcial):** auditoria de snippets AdSense em páginas-chave: home, blog, sobre, contato, serviços, planos e captura-leads já tinham o snippet. Identificadas páginas sem snippet; solução escalável implementada: injeção idempotente do loader AdSense em `assets/js/related-ads.js`, script compartilhado por ~3.600 páginas (commit `d5b0f5e`).
- ✅ **Diagnóstico de deploy:** o site praia.digital é servido pelo repositório-pai `acarolmourad-commits/praia-digital` (GitHub Pages); o fork não tem Pages habilitado e o workflow "Deploy to GitHub Pages" falha no fork (esperado). Aberto **PR #6** (`acarolmourad-commits/praia-digital/pull/6`) levando todas as mudanças do fork ao repositório que serve o site.

### Bloqueios (ação manual necessária)
- ⛔ **Merge do PR #6** — sem isso, as novas páginas e o loader AdSense não entram no ar.
- ⛔ Verificação de propriedade no Search Console (meta `google-site-verification` já está na home; basta confirmar no painel).
- ⛔ Autenticação Gmail/Composio e conta AdSense exigem identidade do proprietário.

### Observações
- Páginas de política/termos não precisam de anúncios (prática recomendada do AdSense); o loader cobre páginas de conteúdo.
- PR #6 está grande (~518 arquivos) porque o fork divergiu do pai; revisar antes do merge.
