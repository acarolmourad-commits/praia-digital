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

Execução manual:
- python scripts/backup_metrics.py

Execução pelo cronjob:
- job_id: 4439d56fcbcb
- workdir: C:/Users/Carolina/praia-digital/litoral-prime-imoveis
- comando: python scripts/backup_metrics.py

Validação:
- O script cria manifest.json com sha256 de cada arquivo copiado.
- Saída esperada: "Backup criado: ...", "Arquivos: ...", "Tamanho: ... bytes", "Manifest: ...".

Restauração de teste validada:
- 34 arquivos copiados para diretório temporário.
- Todos os hashes sha256 conferem com o manifest.
- Produção não foi alterada.

Retenção:
- Sem limpeza automática.
- Backups antigos só são removidos com decisão explícita.

Observações:
- Não commitar a pasta backups/.
- O script não imprime segredos.
- Em caso de falha, ele retorna exit code != 0 e lista avisos.
