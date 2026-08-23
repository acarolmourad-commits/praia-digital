# Guia de Deploy Enterprise — Hermes Agents

> Segurança, escalabilidade, observabilidade e operação de agentes autônomos em ambiente enterprise.  
> Versão 1.0 — 2026-08-23

---

## 1. Visão geral

Este guia cobre o deploy de Hermes Agents em ambientes enterprise com requisitos de produção: multi-tenant, alta disponibilidade, conformidade regulatória e integração com stack corporativa existente.

Requisitos mínimos:
- Kubernetes 1.28+ ou Docker Swarm 1.24+
- PostgreSQL 15+ com replicação
- Redis 7+ (cluster opcional para alta disponibilidade)
- Node de observabilidade: Prometheus + Grafana + Loki ou stack equivalente
- Vault (HashiCorp ou AWS Secrets Manager) para segredos

---

## 2. Segurança

### 2.1 Autenticação e autorização

**Camadas obrigatórias:**

1. **API Gateway** — TLS 1.3, WAF, rate limiting por IP/tenant.
2. **Service-to-Service** — mTLS ou JWT com assinatura assimétrica (RS256). Nunca usar tokens simétricos entre serviços internos.
3. **RBAC granular** — permissões por agente, ferramenta e tenant:

```yaml
# exemplo de policy
rules:
  - agent_id: "agente-atendimento"
    tools: ["crm.read", "calendar.read"]
    tenants: ["acme", "beta-corp"]
    deny_tools: ["crm.delete", "billing.write"]
```

**Proteção de dados sensíveis:**
- Mascaramento automático de CPF, e-mail e telefone em logs e índices vetoriais.
- Criptografia at-rest (AES-256) para Context Store e Vector Store.
- Rotação de chaves a cada 90 dias; chaves antigas mantidas por 7 dias (grace period).

### 2.2 Rede

- **Zero trust:** nenhum serviço confia em outro apenas por estar na mesma VPC.
- **Network policies:** permitir apenas portas e protocolos explícitos entre namespaces.
- **Private endpoints:** APIs externas (CRM, ERP) chamadas via private link ou NAT Gateway; nunca via IP público direto.
- **DNS interno:** resolver `*.internal.praiadigital.com` via CoreDNS com DNSSEC.

### 2.3 Compliance

| Requisito | Implementação |
|-----------|---------------|
| LGPD / GDPR | Anonimização antes de indexação; direito ao esquecimento via `/v1/memory/forget` |
| Logs imutáveis | Write-only bucket S3 ou GCS com retenção de 2 anos |
| Auditoria | Registrar `actor_id`, `action`, `resource_id`, `timestamp`, `ip`, `user_agent` |
| Encryption in transit | TLS 1.3 obrigatório; TLS 1.2 permitido apenas para sistemas legados |
| Penetration testing | Testes semestrais por equipe independente |

### 2.4 Segurança de dependências

- Dependências escaneadas por SCA (Dependabot ou Snyk) em cada PR.
- Build assinado com Sigstore/cosign; imagens verificadas no deploy.
- Sem secrets em Dockerfiles, variáveis de ambiente não-criptografadas ou repositórios públicos.

---

## 3. Arquitetura de deploy

### 3.1 Topologia recomendada

```
Internet
    |
    v
[CDN / WAF]
    |
    v
[API Gateway — Kong / AWS API Gateway]
    |
    +---> [Ingest Service] --+--> [Redis Streams]
    |                        |
    +---> [Orchestrator] ----+--> [PostgreSQL]
    |                        |
    +---> [Agents Pool] -----+--> [Vector Store (Qdrant/Pinecone)]
    |                        |
    +---> [Tool Runner] -----+--> [Vault]
    |
    v
[Observabilidade Stack]
    +---> Prometheus + Grafana
    +---> Loki (logs)
    +---> Jaeger (traces)
```

### 3.2 Multi-tenancy

Estratégia: **schema-per-tenant** no PostgreSQL + namespaces Kubernetes separados.

```
hermes_tenant_acme
hermes_tenant_beta_corp
hermes_tenant_gamma
```

Isolamento de dados:
- Cada tenant tem `tenant_id` em todas as tabelas.
- Row-level security (RLS) no PostgreSQL: políticas por tenant.
- Fila de eventos particionada por `tenant_id`.

### 3.3 Modelos de deploy

**A. Kubernetes (recomendado para enterprise)**

```yaml
# exemplo: Deployment do Orchestrator
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hermes-orchestrator
  namespace: hermes-production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hermes-orchestrator
  template:
    metadata:
      labels:
        app: hermes-orchestrator
    spec:
      serviceAccountName: hermes-orchestrator
      containers:
      - name: orchestrator
        image: praiadigital/hermes-orchestrator:1.4.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: hermes-secrets
              key: database-url
        - name: VAULT_ADDR
          value: "https://vault.internal.praiadigital.com:8200"
        resources:
          requests:
            cpu: "500m"
            memory: "512Mi"
          limits:
            cpu: "2000m"
            memory: "2Gi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 20
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
```

**B. Docker Swarm (para stacks menores)**

```bash
# deploy stack
docker stack deploy -c docker-compose.prod.yml hermes

# escalar serviço
docker service scale hermes_orchestrator=5
```

---

## 4. Escalabilidade

### 4.1 Horizontal scaling

- **Stateless services** (Ingest, API Gateway): escalam via HPA (Horizontal Pod Autoscaler) baseado em CPU/memória ou fila depth.
- **Stateful services** (PostgreSQL, Redis): usar replicas read-only + connection pooling (PgBouncer).

Exemplo HPA:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: hermes-ingest-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: hermes-ingest
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: External
    external:
      metric:
        name: queue_messages_ready
        selector:
          matchLabels:
            queue: ingest
      target:
        type: AverageValue
        averageValue: "100"
```

### 4.2 Throughput alvo

| Camada | Throughput alvo | Latência P99 |
|--------|----------------|--------------|
| API Gateway | 10.000 req/s | 50ms |
| Ingest Layer | 5.000 eventos/s | 100ms |
| Orchestrator | 2.000 runs/s | 800ms |
| Tool Runner | 1.500 calls/s | 2s |

### 4.3 Cache e performance

- **Redis Cluster** para sessão e rate limiting.
- **CDN** para assets estáticos e endpoints públicos de webhook.
- **Connection pooling** obrigatório em todas as conexões com banco.

---

## 5. Observabilidade

### 5.1 Métricas obrigatórias

| Métrica | Tipo | Descrição |
|---------|------|-----------|
| `agent_runs_total` | Counter | Total de execuções por agente e status |
| `agent_run_duration_seconds` | Histogram | Duração de runs (P50, P95, P99) |
| `tool_calls_total` | Counter | Chamadas de ferramenta por nome e status |
| `tool_latency_seconds` | Histogram | Latência de cada ferramenta |
| `webhook_deliveries_total` | Counter | Webhooks enviados / falhos |
| `memory_ops_total` | Counter | Operações de memória (store, search, forget) |
| `queue_depth` | Gauge | Mensagens na fila por tenant |
| `billing_tokens_used` | Counter | Tokens LLM consumidos por tenant |

Alertas críticos:

```yaml
# exemplo de regra Prometheus
groups:
- name: hermes-critical
  rules:
  - alert: HighErrorRate
    expr: rate(agent_run_failed_total[5m]) / rate(agent_run_total[5m]) > 0.05
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "Taxa de erro > 5% nos últimos 5 min"
  - alert: QueueBacklog
    expr: queue_depth > 5000
    for: 5m
    labels:
      severity: warning
```

### 5.2 Logs estruturados

Formato: JSON Lines (NDJSON) com campos obrigatórios:

```json
{
  "timestamp": "2026-08-23T14:32:01.123Z",
  "level": "info",
  "service": "orchestrator",
  "tenant_id": "acme",
  "run_id": "run_8f3k2...",
  "agent_id": "agente-atendimento",
  "event": "run.completed",
  "duration_ms": 1240,
  "tool_calls": 3,
  "trace_id": "abc123...",
  "span_id": "def456..."
}
```

Retenção:
- Logs frios: 90 dias em object storage.
- Logs quentes: 7 dias em Loki/Elasticsearch.

### 5.3 Tracing distribuído

- Usar OpenTelemetry SDK em todos os serviços.
- Exportar para Jaeger ou AWS X-Ray.
- Correlacionar trace_id entre API Gateway, Orchestrator, Agent e Tool Runner.

Exemplo de inicialização Python:

```python
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://jaeger:4317"))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
```

---

## 6. Backups e recuperação

- **PostgreSQL**: WAL archiving + base backup diário; PITR (Point-in-Time Recovery) habilitado.
- **Redis**: RDB snapshot a cada 6h + AOF.
- **Vector Store**: snapshot semanal + exportação contínua de vetores alterados.
- **Disaster Recovery**: réplica cruzada em região secundária com RTO < 4h e RPO < 15min.

Testes de recuperação:
- Simular falha de região trimestralmente.
- Validar restauração de banco e busca vetorial mensalmente.

---

## 7. Operação e runbooks

### 7.1 Runbooks essenciais

| Cenário | Ação |
|---------|------|
| Fila de ingest congestionada | Aumentar réplicas do Ingest Service; verificar dead-letter queue |
| Latência alta em tool calls | Verificar timeout do adapter; checar saúde do serviço externo |
| Falha massiva de webhooks | Verificar endpoint do cliente; checar connectivity; acionar dead-letter |
| Consumo excessivo de tokens LLM | Revisar prompts dos agentes; habilitar cache de embeddings |
| Queda de banco | Failover para réplica; verificar WAL replay |

### 7.2 Manutenção

- Janelas de manutenção: terças e quintas, 02h–04h (horário de menor tráfego).
- Rolling updates: atualizar um pod por vez; esperar readiness probe antes do próximo.
- Blue/Green deploy recomendado para mudanças no schema de API.

---

## 8. Checklist de deploy

- [ ] Vault configurado com segredos rotacionados
- [ ] TLS 1.3 em todos os endpoints públicos
- [ ] Network policies aplicadas por namespace
- [ ] PostgreSQL com replicação e PITR
- [ ] Redis cluster com senha e TLS
- [ ] Prometheus + Alertmanager configurados
- [ ] Loki coletando logs de todos os serviços
- [ ] Jaeger com amostragem de 10% em produção
- [ ] HPA configurado para Ingest e Orchestrator
- [ ] Dead-letter queue monitorada
- [ ] Backup testado nos últimos 30 dias
- [ ] Runbooks documentados e revisados
- [ ] Pen test agendado

---

## 9. Custo estimado (referência)

Para 10 tenants enterprise, 50.000 runs/mês:

| Recurso | Custo mensal (USD) |
|---------|-------------------|
| Kubernetes (EKS/GKE/AKS) | $400–$800 |
| PostgreSQL (RDS/CloudSQL) | $300–$600 |
| Redis (ElastiCache/Memorystore) | $150–$300 |
| Vault (HCP ou self-hosted) | $200–$500 |
| LLM API (tokens) | $800–$2.000 |
| Observabilidade (Grafana Cloud) | $200–$400 |
| CDN + WAF | $100–$200 |
| **Total** | **$2.150–$4.800** |

---

## 10. Links úteis

- [Helm Charts](https://charts.praiadigital.com)
- [Terraform Modules](https://registry.terraform.io/namespaces/praiadigital)
- [Playbook de Incidentes](https://wiki.praiadigital.com/runbooks/hermes)
- [Status Page](https://status.praiadigital.com)
