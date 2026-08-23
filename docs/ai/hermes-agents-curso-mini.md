# Mini-Curso: Agentes Autônomos em 5 Módulos

> Objetivo: dar uma base sólida, prática e orientada a resultados para quem quer entender e implementar agentes autônomos — sem enrolação e com aplicação imediata.

---

## Módulo 1 — O que é um agente autônomo?

### Objetivo
Entender a diferença entre um agente e um software tradicional.

### Conteúdo
- **Software tradicional**: entrada → processamento → saída.
- **Agente autônomo**: entrada → raciocínio → ação → observação → novo raciocínio → ...
- **Loop autônomo**: perceber, decidir, agir e avaliar.
- **Quando usar um agente**: quando a tarefa exige decisões em múltiplos passos, memória ou adaptação.
- **Quando NÃO usar**: quando uma simples função ou API resolve.

### Conceitos-chave
- Agente
- Ambiente
- Ação
- Observação
- Objetivo

### Exercício rápido
Liste 3 tarefas do seu dia a dia que poderiam ser resolvidas por um agente autônomo.

---

## Módulo 2 — Arquitetura essencial de agentes

### Objetivo
Conhecer os componentes básicos de um agente e como eles se conectam.

### Conteúdo
- **Percepção**: entrada de dados, sensores, leitura de contexto.
- **Memória**: curto prazo, longo prazo e memoria de trabalho.
- **Raciocínio**: planejamento, tomada de decisão, seleção de ferramentas.
- **Ação**: execução de comandos, chamadas de API, escrita em arquivos.
- **Avaliação**: métricas, validação e correção.

### Diagrama mental
```
Percepção → Memória → Raciocínio → Ação → Avaliação → (volta para Percepção)
```

### Exercício rápido
Desenhe o fluxo de um agente que:
1. recebe um pedido de e-mail,
2. busca informações,
3. redige a resposta,
4. envia o e-mail.

---

## Módulo 3 — Tipos de agentes e quando usar cada um

### Objetivo
Saber escolher o tipo certo de agente para o problema certo.

### Conteúdo
- **Agente reativo**: responde a estímulos sem memória.
- **Agente baseado em modelo**: mantém estado interno.
- **Agente deliberativo**: planeja antes de agir.
- **Agente com ferramentas**: usa APIs, busca web, executa código.
- **Agente multiagente**: vários agentes cooperando.

### Critérios de escolha
- Complexidade da tarefa
- Necessidade de memória
- Necessidade de múltiplas ferramentas
- Latência aceitável

### Exercício rápido
Classifique os exemplos abaixo como reativo, deliberativo ou com ferramentas.

---

## Módulo 4 — Implementação prática: do prompt ao código

### Objetivo
Colocar a mão na massa com um exemplo mínimo, funcional e replicável.

### Conteúdo
- Estrutura básica de um agente em Python
- Uso de LLM como núcleo de raciocínio
- Loop de execução
- Tratamento de erros e logs
- Adicionando ferramentas simples

### Exemplo mínimo
```python
import json

def agente(objetivo, estado):
    while not objetivo_atingido(objetivo, estado):
        acao = planejar(objetivo, estado)
        resultado = executar(acao)
        estado = atualizar(estado, resultado)
    return estado
```

### Exercício prático
Implemente um agente que:
1. receba um tema,
2. pesquise 3 fontes,
3. gere um resumo,
4. salve em `resumo.md`.

---

## Módulo 5 — Operação, testes e entrega

### Objetivo
Aprender a rodar um agente em produção com qualidade.

### Conteúdo
- **Testes**: unitários, de integração e de fluxo.
- **Observabilidade**: logs estruturados, tracing, métricas.
- **Segurança**: permissões, limites e validação de saída.
- **Deploy**: empacotamento, agendamento, versionamento.
- **Documentação**: README, exemplos de uso, troubleshooting.

### Checklist de entrega
- [ ] Código versionado
- [ ] Testes passando
- [ ] Logs estruturados
- [ ] Limites definidos
- [ ] Documentação atualizada

### Exercício final
Entregue um agente completo com README, testes e exemplo de execução.

---

## Próximos passos
- Estude prompt engineering e agent patterns.
- Pratique com projetos pequenos antes de escalar.
- Participe de comunidades e contribua com exemplos reais.
