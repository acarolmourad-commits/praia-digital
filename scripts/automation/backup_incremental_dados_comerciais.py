
import os, shutil, datetime, csv, hashlib, json, glob
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital')
BACKUP_DIR = BASE / 'docs' / 'sales' / 'backups'
MANIFEST = BACKUP_DIR / 'manifest_backups.json'

ARQUIVOS_COMERCIAIS = [
    BASE / 'docs' / 'sales' / 'followup-registro.md',
    BASE / 'docs' / 'sales' / 'parcerias-leads-capturados.csv',
    BASE / 'docs' / 'sales' / 'leads-litoral-enriquecido.csv',
    BASE / 'docs' / 'sales' / 'leads-litoral-enriquecido-realista.csv',
    BASE / 'docs' / 'sales' / 'csv-lotes-email' / 'lote-brevo-leads-capturados-2026-07-12.csv',
    BASE / 'docs' / 'sales' / 'csv-lotes-email' / 'lote-smtp-50-oficial-2026-07-12.csv',
    BASE / 'docs' / 'sales' / 'tracking-envios-lote-50-2026-07-12.csv',
    BASE / 'docs' / 'sales' / 'leads-priorizados-2026-07-12.csv',
    BASE / 'docs' / 'sales' / 'briefing-matinal-comercial-praia-digital.html',
    BASE / 'docs' / 'sales' / 'top-leads-prontas-2026-07-12.html',
    BASE / 'docs' / 'sales' / 'pacote-execucao-final-2026-07-12.html',
]

EXTENSOES_ALVO = {'.csv', '.md', '.html', '.json'}

sha256 = lambda path: hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None

def carregar_manifest():
    if MANIFEST.exists():
        try:
            return json.loads(MANIFEST.read_text(encoding='utf-8'))
        except Exception:
            return {}
    return {}

def salvar_manifest(manifest):
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')

def arquivo_mudou(caminho: Path, hash_salvo: str):
    if not caminho.exists():
        return False
    return sha256(caminho) != hash_salvo

def backup_arquivo(caminho: Path, destino: Path):
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(caminho, destino)

def main():
    hoje = datetime.datetime.now().strftime('%Y-%m-%d')
    pasta_dia = BACKUP_DIR / f'backup-{hoje}'
    pasta_dia.mkdir(parents=True, exist_ok=True)

    manifest = carregar_manifest()
    atualizados = []
    ignorados = []

    for caminho in ARQUIVOS_COMERCIAIS:
        if not caminho.exists():
            continue
        rel = str(caminho.relative_to(BASE))
        entrada = manifest.get(rel, {})
        hash_salvo = entrada.get('sha256')
        if arquivo_mudou(caminho, hash_salvo):
            destino = pasta_dia / caminho.name
            backup_arquivo(caminho, destino)
            atualizados.append(rel)
            manifest[rel] = {
                'sha256': sha256(caminho),
                'ultimo_backup': hoje,
                'tamanho_bytes': caminho.stat().st_size,
            }
        else:
            ignorados.append(rel)

    # backup de followups pendentes se houver mudanças na pasta
    followup_dir = BASE / 'outreach' / 'followups-pendentes'
    if followup_dir.exists():
        backup_followup = pasta_dia / 'followups-pendentes'
        backup_followup.mkdir(exist_ok=True)
        count = 0
        for file in followup_dir.glob('*.*'):
            if file.suffix.lower() in EXTENSOES_ALVO:
                backup_arquivo(file, backup_followup / file.name)
                count += 1
        if count:
            atualizados.append('outreach/followups-pendentes/*')

    salvar_manifest(manifest)
    resumo = {
        'data_execucao': hoje,
        'atualizados': atualizados,
        'ignorados': ignorados,
        'total_atualizados': len(atualizados),
        'total_ignorados': len(ignorados),
        'pasta_backup': str(pasta_dia),
    }
    print(json.dumps(resumo, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
