# Backup de métricas — Litoral Prime Imóveis

Fonte oficial:
- outreach/metricas.csv
- docs/chat-log-litoral-prime.json
- docs/relatorio-diario-litoral-prime.html
- docs/leads-litoral-prime.csv
- outreach/leads-site.csv
- outreach/do-dia/*/*.csv

Script:
- scripts/backup_metrics.py

Destino:
- backups/metricas/<YYYYMMDD_HHMMSS>/

Execução:
- python scripts/backup_metrics.py

Validação:
- O script cria manifest.json com sha256 de cada arquivo copiado.
- Saída esperada: "Backup criado: ...", "Arquivos: ...", "Tamanho: ... bytes", "Manifest: ...".

Restauração de teste:
1. Copie o snapshot desejado para uma pasta temporária fora do projeto.
2. Valide os hashes no manifest.json.
3. Confira contagem de linhas/CSV e conteúdo do chat-log/relatório.
4. Nunca sobrescreva a pasta original do projeto durante o teste.

Retenção:
- Sem limpeza automática.
- Backups antigos só são removidos com decisão explícita.

Observações:
- Não commitar a pasta backups/.
- O script não imprime segredos.
- Em caso de falha, ele retorna exit code != 0 e lista avisos.
