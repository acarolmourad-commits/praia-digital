# Guia de Instâncias Hermes Especializadas

Este documento descreve como usar perfis especializados do Hermes Agent para separar contextos de trabalho (vendas, conteúdo/SEO, etc.). Cada instância vive em seu próprio diretório de perfil, com sessões, memórias, skills e ferramentas isoladas.

## Perfis Criados

| Perfil | Caminho | Foco |
|--------|---------|------|
| `hermes-sales` | `C:\Users\Carolina\AppData\Local\hermes\profiles\hermes-sales` | Vendas, prospecção, follow-up, pipeline e outreach |
| `hermes-content` | `C:\Users\Carolina\AppData\Local\hermes\profiles\hermes-content` | Conteúdo, SEO, copywriting, GEO e produção editorial |

Ambos compartilham a mesma base de modelo (`stepfun/step-3.7-flash:free` via provider `nous`), mas possuem personalidades, toolsets e prioridades diferentes.

## Estrutura de um Perfil

```
C:\Users\Carolina\AppData\Local\hermes\profiles\<nome-do-perfil>\
├── config.yaml        # Configuração isolada do perfil
├── skills\            # Skills exclusivas (se houver)
├── plugins\           # Plugins exclusivos (se houver)
├── cron\              # Cron jobs exclusivos (se houver)
└── memories\          # Memórias persistentes isoladas
```

## Como Usar

### 1. Listar perfis disponíveis

```bash
hermes profile list
```

### 2. Usar um perfil específico (sessão ad-hoc)

```bash
# Vendas
hermes chat --profile hermes-sales

# Conteúdo/SEO
hermes chat --profile hermes-content
```

### 3. Definir perfil padrão

```bash
hermes profile use hermes-sales
```

### 4. Clonar ou modificar perfis

```bash
# Criar novo perfil a partir do existente
hermes profile create novo-perfil --clone-from hermes-sales

# Renomear
hermes profile rename hermes-sales hermes-vendas

# Exportar / importar
hermes profile export hermes-sales -o ~/backups/hermes-sales.tar.gz
hermes profile import ~/backups/hermes-sales.tar.gz
```

## Diferenças entre os Perfis

### hermes-sales
- **Ferramentas ativadas:** `web`, `search`, `browser`, `terminal`, `messaging`, `kanban`, `file`, `session_search`
- **Personalidade padrão:** `sales` (consultativa, focada em pipeline e fechamento)
- **Uso ideal:**
  - Prospecção de leads e clientes
  - Follow-up de cotações e reuniões
  - Gestão de pipeline (kanban)
  - Envio de mensagens via gateway
  - Pesquisa de mercado e concorrentes

### hermes-content
- **Ferramentas ativadas:** `web`, `search`, `browser`, `file`, `vision`, `image_gen`, `session_search`
- **Personalidade padrão:** `content_seo` (focada em SEO, GEO, estrutura e copy)
- **Uso ideal:**
  - Produção de artigos e posts
  - Pesquisa de palavras-chave e SERPs
  - Geração de imagens para conteúdo
  - Auditoria e otimização SEO
  - Reescrita e adaptação de copy

## Boas Práticas

1. **Separação de contexto:** Nunca misture conversas de vendas com produção editorial. Cada perfil mantém seu próprio histórico e memória.
2. **Skills exclusivas:** Instale skills específicas de cada domínio no diretório `skills/` do perfil correspondente.
3. **Cron jobs isolados:** Agende follow-ups de vendas no perfil `hermes-sales` e publicações de conteúdo no `hermes-content`.
4. **Memória compartilhada com cuidado:** Cada perfil tem sua memória própria. Se precisar cruzar dados, exporte manualmente.
5. **Modelos diferentes por perfil:** Se quiser, edite o `config.yaml` de cada perfil para usar modelos distintos (`model.default` e `model.provider`).

## Exemplo de Edição Rápida

```bash
# Abrir config do perfil de vendas
hermes config edit --profile hermes-sales

# Definir modelo diferente apenas para conteúdo
hermes config set --profile hermes-content model.default anthropic/claude-sonnet-4
```

## Troubleshooting

- **Perfil não aparece:** execute `hermes profile list` e confira o nome da pasta em `C:\Users\Carolina\AppData\Local\hermes\profiles\`.
- **Mudanças não aplicam:** reinicie a sessão (`/reset` no chat) ou saia e entre novamente com `--profile`.
- **Ferramentas ausentes:** use `hermes tools list --profile hermes-sales` para ver o que está habilitado.
