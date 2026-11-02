#!/usr/bin/env python3
"""Read public Sentinela state into a non-published review artifact containing public sources only, never published editions.
No network fetch, mutations of Sentinela, or subscriber data. Run daily to surface
missing sources and editorial candidates. Detection time is NOT publication time.
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def prepare(root=ROOT):
    state_path = root / 'automation/marketplaces/sentinela-estado.json'
    checked = datetime.now(timezone.utc).isoformat()
    if not state_path.exists():
        return {'prepared_at': checked, 'status': 'source_state_missing', 'candidates': [], 'sources': []}
    state = json.loads(state_path.read_text(encoding='utf-8'))
    candidates = []
    for article in state.get('articles', []):
        candidates.append({'status': 'needs_editorial_review', 'title': article.get('title'), 'detected_at_unverified': article.get('date'), 'source_url': article.get('source'), 'local_article': article.get('file'), 'published_at': None, 'review_notes': 'Read original source; verify publication date, local relevance, duplicates and actual change. A hash change is not a news event.'})
    sources = [{'id': key, 'url': source.get('url'), 'last_recorded_http_status': source.get('status'), 'unavailable': source.get('unavailable', False)} for key, source in state.get('sources', {}).items()]
    return {'prepared_at': checked, 'status': 'review_required', 'notice': 'Preparation timestamp is not a fresh verification of the remote source. No content was published.', 'sources': sources, 'candidates': candidates}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args(); args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(prepare(), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
