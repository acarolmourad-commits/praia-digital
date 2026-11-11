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

def editorial_state(root, as_of):
    """Flag stale editions and deadlines using saved records, without fetching or publishing."""
    editions = [json.loads(p.read_text(encoding='utf-8')) for p in sorted((root / 'data/boletim/edicoes').glob('*.json'))]
    reviewed = [e for e in editions if e.get('status') == 'reviewed']
    if not reviewed:
        return {'status': 'no_reviewed_edition', 'deadlines': []}
    latest = max(reviewed, key=lambda e: e['date'])
    last_review = datetime.fromisoformat(latest['reviewed_at'].replace('Z', '+00:00'))
    deadlines = []
    for edition in reviewed:
        for item in edition['items']:
            if not item.get('deadline'):
                continue
            deadline = datetime.strptime(item['deadline'], '%Y-%m-%d').date()
            remaining = (deadline - as_of.date()).days
            has_note = any(datetime.fromisoformat(u['noted_at'].replace('Z', '+00:00')).date() > deadline for u in item.get('updates', []))
            deadlines.append({'edition': edition['date'], 'item_id': item['id'], 'source_url': item['source_url'], 'deadline': item['deadline'], 'days_remaining': remaining, 'status': 'deadline_passed' if remaining < 0 else 'upcoming', 'has_later_editorial_note': has_note, 'needs_review': (remaining < 0 and not has_note) or 0 <= remaining <= 7})
    return {'status': 'manual_review_required', 'latest_edition': latest['date'], 'last_editorial_review': latest['reviewed_at'], 'days_since_last_review': (as_of.date() - last_review.date()).days, 'deadlines': deadlines, 'notice': 'This is an operational check of saved dates, not a new verification of sources or an automatic publication.'}

def prepare(root=ROOT, as_of=None):
    state_path = root / 'automation/marketplaces/sentinela-estado.json'
    now = as_of or datetime.now(timezone.utc)
    checked = now.isoformat()
    editorial = editorial_state(root, now)
    if not state_path.exists():
        return {'prepared_at': checked, 'status': 'source_state_missing', 'candidates': [], 'sources': [], 'editorial': editorial}
    state = json.loads(state_path.read_text(encoding='utf-8'))
    candidates = []
    for article in state.get('articles', []):
        candidates.append({'status': 'needs_editorial_review', 'title': article.get('title'), 'detected_at_unverified': article.get('date'), 'source_url': article.get('source'), 'local_article': article.get('file'), 'published_at': None, 'review_notes': 'Read original source; verify publication date, local relevance, duplicates and actual change. A hash change is not a news event.'})
    sources = [{'id': key, 'url': source.get('url'), 'last_recorded_http_status': source.get('status'), 'unavailable': source.get('unavailable', False)} for key, source in state.get('sources', {}).items()]
    return {'prepared_at': checked, 'status': 'review_required', 'notice': 'Preparation timestamp is not a fresh verification of the remote source. No content was published.', 'sources': sources, 'candidates': candidates, 'editorial': editorial}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args(); args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(prepare(), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
