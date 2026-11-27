"""Offline external-link planner. Never resolves DNS or performs HTTP.

This prepares reviewable batches; it does not authorize or execute them.
History is an explicit input, not a best-effort cache of presumed successes.
"""
from collections import Counter
import datetime
import math
from urllib.parse import urlsplit

MAX_URLS = 80
MAX_PER_HOST = 20
PRIORITY_SLOTS = 20
UTC = datetime.timezone.utc


def page_priority(page):
    """Business importance is a heuristic, never proof of publication."""
    parts = page.lower().split('/')
    if any(part in ('backup', 'backups', 'templates') for part in parts):
        return 0
    if page in ('index.html', 'servicos.html', 'imoveis.html', 'contato.html',
                'cadastrar-imovel.html', 'solicitar-servico.html'):
        return 3
    if page.startswith(('compras/', 'afiliados/', 'academy/', 'imoveis/',
                        'servicos/', 'planos', 'proprietarios/')):
        return 3
    if page.startswith(('apps/', 'ferramentas/')):
        return 2
    return 1


def timestamp(value):
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value < 0:
        raise ValueError('Invalid history timestamp')
    return value


def validate_history(history):
    if not isinstance(history, dict) or history.get('version') != 1:
        raise ValueError('Expected history version 1; do not silently reset history')
    entries, hosts = history.get('urls'), history.get('hosts')
    if not isinstance(entries, dict) or not isinstance(hosts, dict):
        raise ValueError('Expected urls and hosts maps')
    for entry in entries.values():
        if not isinstance(entry, dict):
            raise ValueError('Invalid history entry')
        for field in ('last_attempt', 'last_http_response', 'retry_after_until'):
            if field in entry:
                timestamp(entry[field])
        if 'last_http_response' in entry and 'last_attempt' not in entry:
            raise ValueError('HTTP response without an attempt')
        if entry.get('last_http_response', 0) > entry.get('last_attempt', 0):
            raise ValueError('HTTP response after last attempt')
        if not isinstance(entry.get('category', ''), str):
            raise ValueError('Invalid history category')
    for until in hosts.values():
        timestamp(until)
    return entries, hosts


def due_at(entry, priority):
    if 'last_attempt' not in entry:
        return entry.get('retry_after_until', 0)
    category = entry.get('category', '')
    if category in ('restricted', 'access_blocked', 'not_checked'):
        hours = 168
    elif category == 'rate_limited':
        hours = 24
    elif category in ('network_error', 'transient', 'transient_http'):
        hours = 6
    elif category == 'broken':
        hours = 24
    else:
        hours = 24 if priority >= 2 else 24 * 14
    return max(entry['last_attempt'] + hours * 3600,
               entry.get('retry_after_until', 0))


def plan_external(urls, history, now, limit=MAX_URLS,
                  priority_slots=PRIORITY_SLOTS, per_host=MAX_PER_HOST):
    """Reserve risk slots, then fill by oldest attempt with a per-host cap.

    An unseen URL sorts before an attempted URL. No weekly index depends on
    the inventory length, so inserting a URL does not reset a rotation.
    """
    if now.tzinfo is None:
        raise ValueError('Expected timezone-aware now')
    for value, ceiling in ((limit, MAX_URLS), (priority_slots, MAX_URLS),
                           (per_host, MAX_PER_HOST)):
        if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= ceiling:
            raise ValueError('Invalid batch limit')
    if limit == 0 or per_host == 0:
        raise ValueError('Batch and host limits must be positive')
    entries, hosts = validate_history(history)
    clock = now.timestamp()
    eligible, deferred = [], Counter()
    for url, meta in sorted(urls.items()):
        parts = urlsplit(url)
        if parts.scheme not in ('http', 'https') or not parts.hostname or parts.username is not None or parts.password is not None:
            deferred['invalid_url'] += 1
            continue
        host = parts.hostname.lower()
        priority = meta.get('priority', page_priority(meta.get('page', '')))
        if not isinstance(priority, int) or not 0 <= priority <= 3:
            raise ValueError('Invalid priority')
        entry = entries.get(url, {})
        if hosts.get(host, 0) > clock:
            deferred['host_cooldown'] += 1
            continue
        if due_at(entry, priority) > clock:
            deferred['not_due'] += 1
            continue
        eligible.append({'url': url, 'host': host, 'priority': priority,
                         'page': meta.get('priority_page', meta.get('page', '')),
                         'last_attempt': entry.get('last_attempt'),
                         'risk': priority >= 2 or entry.get('category') in
                         ('broken', 'network_error', 'transient', 'transient_http')})
    selected, chosen, host_counts = [], set(), Counter()

    def oldest(item):
        return (item['last_attempt'] is not None, item['last_attempt'] or 0, item['url'])

    def take(items, maximum, lane):
        # A busy commercial host must not consume its whole quota in the
        # reserved lane and indefinitely starve ordinary URLs on that host.
        host_limit = max(1, per_host // 4) if lane == 'risk' else per_host
        for item in items:
            if len(selected) >= maximum:
                break
            if item['url'] in chosen or host_counts[item['host']] >= host_limit:
                continue
            selected.append({**item, 'lane': lane})
            chosen.add(item['url'])
            host_counts[item['host']] += 1

    take(sorted((x for x in eligible if x['risk']),
                key=lambda x: (*oldest(x)[:2], -x['priority'], x['url'])),
         min(limit, priority_slots), 'risk')
    take(sorted(eligible, key=oldest), limit, 'breadth')
    return {'version': 1, 'mode': 'offline_plan', 'generated_at': now.astimezone(UTC).isoformat(),
            'network_performed': False, 'candidates': len(urls), 'eligible': len(eligible),
            'selected': len(selected), 'deferred': dict(deferred),
            'eligible_not_selected': len(eligible) - len(selected),
            'limits': {'urls_per_run': limit, 'urls_per_host': per_host,
                       'reserved_risk_slots': min(limit, priority_slots)},
            'host_counts': dict(host_counts), 'results': selected,
            'coverage_note': 'Planning is not HTTP validation. URL caps do not count redirect or GET requests. '
                             'Execution needs a request governor and persistent cooldowns before activation.'}
