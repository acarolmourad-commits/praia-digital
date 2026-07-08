# Praia Digital API

Serviços de IA para imobiliárias do litoral paulista.

## Como rodar

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Endpoints

- POST /avaliar — avaliação de preço de imóveis
- POST /descrever — geração de descrições
- POST /priorizar — priorização de leads
- GET /health — health check
