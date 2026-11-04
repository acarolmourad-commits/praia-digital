"""Reconcile existing records; owner-retired synthetic seeds are never regenerated."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
from enforce_listing_retirements import retired_slugs

base = Path('litoral-prime-imoveis')
retired = retired_slugs() | {'peruibe-centro-venda'}
dataset = base / 'imoveis/properties.json'
records = json.loads(dataset.read_text(encoding='utf-8')) if dataset.exists() else []
kept = [item for item in records if item.get('slug') not in retired]
dataset.parent.mkdir(parents=True, exist_ok=True)
if records != kept or not dataset.exists():
    dataset.write_text(json.dumps(kept, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

js = base / 'js/main.js'
if js.exists():
    text = js.read_text(encoding='utf-8')
    def clean(match):
        original = json.loads(match[2])
        active = [item for item in original if item.get('slug') not in retired]
        return match[0] if active == original else match[1] + json.dumps(active, ensure_ascii=False, indent=4) + ';'
    updated = re.sub(r'(const properties\s*=\s*)(\[[\s\S]*?\]);', clean, text)
    if updated != text:
        js.write_text(updated, encoding='utf-8')

print('Portfolio preservado:', len(kept), 'registros; nenhum registro sintetico gerado.')
