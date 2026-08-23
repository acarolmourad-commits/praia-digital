# Guia de Segurança e LGPD — Hermes Agents

A Praia Digital adota os mais altos padrões de segurança de dados e governança para garantir total conformidade regulatória e proteção às operações dos nossos clientes.

## Arquitetura de Proteção de Dados

### 1. Criptografia e Armazenamento
- Dados em Trânsito: Criptografia obrigatória via TLS 1.3 / HTTPS em todas as comunicações via API, Webhooks e Canais (WhatsApp/Instagram).
- Dados em Repouso: Bancos de dados criptografados utilizando padrão AES-256.
- Isolamento de Tenant: Arquitetura *multi-tenant* logicamente isolada, garantindo que os dados de cada empresa sejam totalmente inacessíveis por terceiros.

### 2. Conformidade LGPD (Lei Geral de Proteção de Dados)
- Minimização de Dados: Coleta estritamente limitada às informações necessárias para a execução do agente.
- Anonimização & Pseudo-anonimização: Filtros nativos antes do envio de prompts para os modelos de IA para omitir CPF, dados bancários e informações sensíveis não autorizadas.
- Direito do Titular: Ferramentas nativas para exportação, retificação e exclusão definitiva de dados a pedido do usuário final.
- Trilha de Auditoria: Log completo e imutável de todas as ações executadas pelos agentes autônomos.

### 3. Governança e Controle de Acesso
- Autenticação baseada em funções (RBAC) com suporte a duplo fator (2FA).
- Testes recorrentes de intrusão e varreduras de vulnerabilidade na infraestrutura.

---

👉 Sua área de TI ou Compliance precisa de documentação detalhada?
- Consulte nossa [Análise Competitiva de Governança](hermes-agents-competitive-analysis.md).
- Ou [solicite nosso relatório de conformidade e segurança](https://praiadigital.com.br/contato).
