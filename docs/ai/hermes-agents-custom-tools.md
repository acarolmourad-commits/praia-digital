# Ferramentas Customizadas — Hermes Agents

> Como criar ferramentas para agentes autônomos.

## Estrutura
```python
from tools.registry import registry

def minha_tool(param: str) -> str:
    return json.dumps({"success": True, "data": "..."})

registry.register(
    name="minha_tool",
    toolset="custom",
    schema={...},
    handler=lambda args, **kw: minha_tool(param=args.get("param", "")),
    check_fn=lambda: True
)
```

## Tipos
- APIs externas (REST/GraphQL)
- Consultas a banco de dados
- Geração de documentos
- Integração com ERPs

## Boas práticas
- Sempre retorne JSON
- Valide entrada antes de executar
- Trate erros gracefully
- Documente schema completo
