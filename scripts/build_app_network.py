"""Render the same complete app directory on every app. No data or calculations change."""
import argparse
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTES = {
    'comprar': 'Planejar uma compra',
    'locar': 'Comparar locações',
    'anunciar': 'Preparar um anúncio',
    'vender': 'Precificar um produto',
}

def render(groups, current=None, guidance=None):
    esc = html.escape
    titles = {a['slug']: a['title'] for g in groups for a in g['apps']}
    guide = (guidance or {}).get(current)
    catalog_link = '<a href="/apps/">Catálogo de aplicativos</a>'
    if current:
        group = next(group for group in groups if any(app['slug'] == current for app in group['apps']))
        group_id = esc(group['id'])
        catalog_link = (f'<a href="/apps/?objetivo={group_id}#grupo-{group_id}">'
                        f'Catálogo de aplicativos · {esc(group["title"])}</a> · '
                        '<a href="/apps/">Ver o catálogo completo</a>')
    practical = ''
    if guide:
        next_links = ''.join(f'<li><a href="/apps/{esc(slug)}/">{esc(titles[slug])}</a></li>' for slug in guide['next'])
        practical = ('<div class="pd-workflow" aria-labelledby="pd-workflow-title">'
            '<h3 id="pd-workflow-title">Use este resultado na sua rotina</h3>'
            '<dl><div><dt>Antes de começar</dt><dd>' + esc(guide['prepare']) + '</dd></div>'
            '<div><dt>O que registrar</dt><dd>' + esc(guide['record']) + '</dd></div></dl>'
            + '<p class="pd-route-link"><a href="/apps/guia-de-uso.html#' + esc(guide['route']) + '">Abrir roteiro: ' + esc(ROUTES[guide['route']]) + '</a></p>'
            + '<p>Antes de abrir outra ferramenta, <a href="/apps/guia-de-uso.html#qual-arquivo-guardar">guarde uma cópia do que conferiu</a>. Os dados preenchidos não acompanham o link.</p>'
            + ('<p><strong>Continue sua análise</strong></p><ul class="pd-next-links" role="list">' + next_links + '</ul>' if next_links else '<p>Explore outras ferramentas no catálogo ao final desta seção.</p>') + '</div>')
    sections = []
    for group in groups:
        links = []
        for app in group['apps']:
            if app['slug'] == current:
                continue
            links.append(f'<li><a href="/apps/{esc(app["slug"])}/"><strong>{esc(app["title"])}</strong><span>{esc(app["description"])}</span></a></li>')
        if links:
            sections.append(f'<div class="pd-network-group"><h3>{esc(group["title"])}</h3><ul class="pd-network-grid">{"".join(links)}</ul></div>')
    return ('<section class="pd-network" aria-labelledby="pd-network-title">'
            '<h2 id="pd-network-title" tabindex="-1">Continue com o próximo aplicativo</h2>'
            '<p class="pd-network-intro">Use uma ficha conferida, anote suas premissas e escolha o recurso da próxima etapa. Você pode voltar ao catálogo a qualquer momento.</p>'
            + practical + '<details><summary>Explorar a rede completa de aplicativos</summary>' + ''.join(sections) + '</details>'
            '<p><a href="/apps/guia-de-uso.html">Guia prático e checklists</a> · ' + catalog_link + ' · <a href="/#rede-apps">Roteiros na página inicial</a> · <a href="/servicos.html">Apoio profissional</a></p>'
            '<p class="pd-network-note">Os links não transferem dados automaticamente. Confira fontes, datas, custos e limitações antes de decidir. Simulações não são laudos, aprovação de crédito nem garantia de retorno.</p></section>')

def build(root=ROOT, check=False):
    stylesheet = '/css/app-network.css?v=' + hashlib.sha256((root / 'css/app-network.css').read_bytes()).hexdigest()[:12]
    groups = json.loads((root / 'data/app-network.json').read_text(encoding='utf-8'))
    guidance = json.loads((root / 'data/app-guidance.json').read_text(encoding='utf-8'))
    slugs = [a['slug'] for g in groups for a in g['apps']]
    actual = {p.parent.name for p in (root / 'apps').glob('*/index.html')}
    if len(slugs) != len(set(slugs)) or set(slugs) != actual:
        raise ValueError('App registry must match every published app exactly once')
    if set(guidance) != set(slugs):
        raise ValueError('Every app needs practical guidance')
    for slug, guide in guidance.items():
        if not guide['prepare'].strip() or not guide['record'].strip() or any(s not in slugs or s == slug for s in guide['next']):
            raise ValueError('Invalid practical guidance: ' + slug)
        if guide.get('route') not in ROUTES:
            raise ValueError('Invalid guide route: ' + slug)
    changed = []
    for slug in [None] + slugs:
        path = root / 'apps' / (slug or '') / 'index.html'
        text = path.read_text(encoding='utf-8')
        network = render(groups, slug, guidance)
        pattern = r'<section\b[^>]*class="pd-network"[^>]*>[\s\S]*?</section>'
        if re.search(pattern, text):
            updated = re.sub(pattern, lambda _: network, text, count=1)
        else:
            updated = text.replace('</body>', '\n' + network + '\n</body>')
        stylesheet_pattern = r'href="/css/app-network\.css(?:\?[^\"]*)?"'
        if re.search(stylesheet_pattern, updated):
            updated = re.sub(stylesheet_pattern, lambda _: 'href="' + stylesheet + '"', updated)
        else:
            updated = updated.replace('</head>', '<link rel="stylesheet" href="' + stylesheet + '">\n</head>')
        if updated != text:
            changed.append(str(path.relative_to(root)))
            if not check:
                path.write_text(updated, encoding='utf-8')
    return changed

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    changed = build(check=args.check)
    print(json.dumps({'changed': changed}, ensure_ascii=False))
    raise SystemExit(1 if args.check and changed else 0)
