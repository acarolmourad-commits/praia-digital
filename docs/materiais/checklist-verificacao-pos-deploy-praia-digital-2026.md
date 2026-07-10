# Checklist de Verificação Pós-Deploy — Praia Digital

## Objetivo
Garantir que cada deploy não quebrou funcionalidades existentes e que novos recursos estão operacionais.

## Verificações obrigatórias após cada push

- [ ] **Site principal abre corretamente**
  - Acessar: https://acarolmourad-commits.github.io/praia-digital/
  - Verificar: carregamento sem erro, header/footer visíveis

- [ ] **Ferramentas gratuitas operacionais**
  - Acessar: https://praia.digital
  - Verificar: páginas de ferramentas carregam, links internos funcionam

- [ ] **Links internos do site**
  - Navegar por: Início, Blog, Planos, Cases, Ferramentas
  - Verificar: nenhum link quebrado (404)

- [ ] **Widget WhatsApp flutuante**
  - Verificar: botão visível no canto inferior direito
  - Testar: clique abre WhatsApp com mensagem pré-preenchida

- [ ] **Popup de captura de leads**
  - Verificar: popup aparece após X segundos
  - Testar: formulário aceita email e nome
  - Verificar: mensagem de confirmação aparece

- [ ] **Highlight box de conversão**
  - Verificar: botão "+" aparece acima do WhatsApp float
  - Testar: clique abre box com cases/planos/ferramentas
  - Verificar: botão "Fechar" funciona

- [ ] **Blog SEO**
  - Verificar: últimos artigos publicados carregam
  - Testar: links de navegação entre artigos funcionam

- [ ] **Responsivo**
  - Testar em: desktop, tablet e mobile
  - Verificar: layout se adapta, botões são clicáveis

- [ ] **Performance básica**
  - Verificar: página carrega em menos de 5s
  - Verificar: não há erros no console do browser

## Comandos rápidos de validação

```bash
# Contar arquivos deployados
cd C:/Users/Carolina/praia-digital
ls blog | wc -l
ls imoveis | wc -l
ls docs/materiais | wc -l

# Verificar último commit
git log --oneline -1

# Verificar status
git status -s
```

## Ações corretivas comuns

- **Link quebrado:** verificar caminho relativo vs absoluto
- **Widget não aparece:** verificar ordem de carregamento dos scripts no index.html
- **Popup não abre:** verificar se assets/popup-captura-leads.html existe e está carregado
- **Erro 404 em página nova:** verificar se arquivo foi committed e pushed

## Frequência
Executar este checklist após **cada deploy** que modifique:
- index.html
- assets/widgets
- Páginas públicas principais

## Histórico
- 2026-07-10: checklist criado
- Próxima revisão: após próximo deploy
