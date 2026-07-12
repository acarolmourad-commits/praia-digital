
import sys
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital')
sys.path.insert(0, str(BASE / 'scripts' / 'automation'))

steps = [
    ('Backup incremental', 'scripts/automation/backup_incremental_dados_comerciais.py'),
    ('Processar leads do site', 'scripts/automation/processar_novos_leads_site.py'),
    ('Gerar briefing dinâmico', 'scripts/automation/gerar_briefing_dinamico.py'),
    ('Gerar central dinâmica', 'scripts/automation/gerar_central_dinamica.py'),
    ('Verificar funil comercial', 'scripts/automation/verificador_funil_comercial.py'),
    ('Gerar status do funil', 'scripts/automation/gerar_status_funil.py'),
    ('Atualizar sitemap SEO', 'scripts/automation/gerar_sitemap_seo.py'),
    ('Gerar artigos SEO por cidade', 'scripts/automation/gerar_artigos_seo_cidades_2026.py'),
    ('Gerar follow-ups por lead', 'scripts/automation/gerar_followups_leads.py'),
    ('Gerar conteúdo redes sociais', 'scripts/automation/gerar_roteiro_video_diario.py'),
]

print('='*50)
print('  ORQUESTRADOR MESTRE — Praia Digital')
print('='*50)
print()

for idx, (name, script) in enumerate(steps, start=1):
    script_path = BASE / script
    print(f'[{idx}/{len(steps)}] Executando: {name}...')
    if not script_path.exists():
        print(f'  ❌ Script não encontrado: {script}')
        continue
    
    # Executa o script via importação
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(f'step_{idx}', script_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print(f'  ✅ Concluído')
    except SystemExit:
        print(f'  ⚠️  Script finalizou (possível saída programada)')
    except Exception as e:
        print(f'  ❌ Erro: {e}')
    print()

print('='*50)
print('  ROTINA CONCLUÍDA')
print('='*50)
print()
print('Próximo: abra central-comando-praia-digital.html')
